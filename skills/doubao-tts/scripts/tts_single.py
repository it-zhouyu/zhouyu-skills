#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
豆包语音合成 - 单文本生成

用法:
    python tts_single.py "要合成的文本" -o output.mp3
    python tts_single.py "文本内容" -o output.mp3 -v zh_male_chunhou_uranus_bigtts
"""

import argparse
import asyncio
import copy
import json
import logging
import os
import sys
import uuid

# Add lib to path
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(SCRIPT_DIR, '..', 'lib'))

import websockets
from protocols import (
    EventType,
    MsgType,
    finish_connection,
    finish_session,
    receive_message,
    start_connection,
    start_session,
    task_request,
    wait_for_event,
)

# API Configuration - Read from environment variables
APP_ID = os.environ.get("DOUBAO_TTS_APP_ID", "")
ACCESS_TOKEN = os.environ.get("DOUBAO_TTS_ACCESS_TOKEN", "")
ENDPOINT = os.environ.get("DOUBAO_TTS_ENDPOINT", "wss://openspeech.bytedance.com/api/v3/tts/bidirection")

# Default voice
DEFAULT_VOICE = os.environ.get("DOUBAO_TTS_DEFAULT_VOICE", "zh_female_xiaohe_uranus_bigtts")

logging.basicConfig(level=logging.WARNING, format='%(message)s')

def validate_credentials():
    """Check if required credentials are set"""
    if not APP_ID:
        print("✗ 错误: 未设置 DOUBAO_TTS_APP_ID 环境变量")
        print("  请设置: export DOUBAO_TTS_APP_ID='your_app_id'")
        return False
    if not ACCESS_TOKEN:
        print("✗ 错误: 未设置 DOUBAO_TTS_ACCESS_TOKEN 环境变量")
        print("  请设置: export DOUBAO_TTS_ACCESS_TOKEN='your_access_token'")
        return False
    return True

def get_resource_id(voice: str) -> str:
    return "seed-tts-2.0"

async def generate_audio(websocket, text: str, output_path: str, voice_type: str) -> bool:
    base_request = {
        "user": {"uid": str(uuid.uuid4())},
        "namespace": "BidirectionalTTS",
        "req_params": {
            "speaker": voice_type,
            "audio_params": {"format": "mp3", "sample_rate": 24000, "enable_timestamp": True},
            "additions": json.dumps({"disable_markdown_filter": False}),
        },
    }

    start_session_request = copy.deepcopy(base_request)
    start_session_request["event"] = EventType.StartSession
    session_id = str(uuid.uuid4())
    await start_session(websocket, json.dumps(start_session_request).encode(), session_id)

    try:
        await wait_for_event(websocket, MsgType.FullServerResponse, EventType.SessionStarted)
    except Exception as e:
        print(f"✗ Session start failed: {e}")
        return False

    async def send_chars():
        for char in text:
            synthesis_request = copy.deepcopy(base_request)
            synthesis_request["event"] = EventType.TaskRequest
            synthesis_request["req_params"]["text"] = char
            await task_request(websocket, json.dumps(synthesis_request).encode(), session_id)
            await asyncio.sleep(0.005)
        await finish_session(websocket, session_id)

    send_task = asyncio.create_task(send_chars())
    audio_data = bytearray()

    try:
        while True:
            msg = await receive_message(websocket)
            if msg.type == MsgType.FullServerResponse and msg.event == EventType.SessionFinished:
                break
            elif msg.type == MsgType.AudioOnlyServer:
                audio_data.extend(msg.payload)
    except Exception as e:
        print(f"✗ Receive error: {e}")
        await send_task
        return False

    await send_task

    if audio_data:
        # Ensure output directory exists
        os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
        with open(output_path, "wb") as f:
            f.write(audio_data)
        print(f"✓ Saved: {output_path} ({len(audio_data)} bytes)")
        return True
    print("✗ No audio data received")
    return False

async def main():
    parser = argparse.ArgumentParser(description='豆包语音合成 - 单文本生成')
    parser.add_argument('text', help='要合成的文本')
    parser.add_argument('-o', '--output', default='output.mp3', help='输出文件路径 (默认: output.mp3)')
    parser.add_argument('-v', '--voice', default=DEFAULT_VOICE, help=f'音色类型 (默认: {DEFAULT_VOICE})')

    args = parser.parse_args()

    if not validate_credentials():
        sys.exit(1)

    print(f"音色: {args.voice}")
    print(f"输出: {args.output}")
    print(f"文本: {args.text[:50]}{'...' if len(args.text) > 50 else ''}")
    print()

    headers = {
        "X-Api-App-Key": APP_ID,
        "X-Api-Access-Key": ACCESS_TOKEN,
        "X-Api-Resource-Id": get_resource_id(args.voice),
        "X-Api-Connect-Id": str(uuid.uuid4()),
    }

    print("连接服务器...")
    try:
        websocket = await websockets.connect(ENDPOINT, additional_headers=headers, max_size=10 * 1024 * 1024)
        print("✓ 连接成功\n")
    except Exception as e:
        print(f"✗ 连接失败: {e}")
        sys.exit(1)

    try:
        await start_connection(websocket)
        await wait_for_event(websocket, MsgType.FullServerResponse, EventType.ConnectionStarted)

        success = await generate_audio(websocket, args.text, args.output, args.voice)
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"\n✗ 错误: {e}")
        sys.exit(1)
    finally:
        try:
            await finish_connection(websocket)
            await wait_for_event(websocket, MsgType.FullServerResponse, EventType.ConnectionFinished)
        except:
            pass
        await websocket.close()

if __name__ == "__main__":
    asyncio.run(main())