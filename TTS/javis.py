#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
javis.py - 음성 녹음 및 STT 처리 시스템

기능:
1. 마이크 인식 및 음성 녹음
2. STT (Speech to Text) 처리
3. CSV 파일로 텍스트 저장
4. 날짜 범위 검색 (보너스)
5. 키워드 검색 (보너스)
'''

import os
import csv
import wave
import pyaudio
import speech_recognition as sr
from datetime import datetime
from pathlib import Path


class JavisRecorder:
    '''음성 녹음 및 STT 처리 클래스'''

    def __init__(self, records_dir='records'):
        '''
        초기화 함수

        Args:
            records_dir (str): 녹음 파일 저장 디렉토리
        '''
        self.records_dir = records_dir
        self.chunk = 1024
        self.format = pyaudio.paInt16
        self.channels = 1
        self.rate = 16000
        self.recognizer = sr.Recognizer()

        # records 디렉토리 생성
        os.makedirs(self.records_dir, exist_ok=True)

    def list_microphones(self):
        '''사용 가능한 마이크 목록 출력'''
        audio = pyaudio.PyAudio()
        print('\n=== 사용 가능한 마이크 목록 ===')
        for i in range(audio.get_device_count()):
            info = audio.get_device_info_by_index(i)
            if info['maxInputChannels'] > 0:
                print(f'{i}: {info["name"]}')
        audio.terminate()

    def record_audio(self, duration=5, device_index=None):
        '''
        음성 녹음

        Args:
            duration (int): 녹음 시간(초)
            device_index (int): 마이크 디바이스 인덱스

        Returns:
            str: 저장된 파일 경로
        '''
        audio = pyaudio.PyAudio()

        # 파일명 생성: YYYYMMDD-HHMMSS.wav
        timestamp = datetime.now().strftime('%Y%m%d-%H%M%S')
        filename = f'{timestamp}.wav'
        filepath = os.path.join(self.records_dir, filename)

        print(f'\n녹음 시작... ({duration}초)')

        # 스트림 열기
        stream = audio.open(
            format=self.format,
            channels=self.channels,
            rate=self.rate,
            input=True,
            input_device_index=device_index,
            frames_per_buffer=self.chunk
        )

        frames = []

        # 녹음
        for i in range(0, int(self.rate / self.chunk * duration)):
            data = stream.read(self.chunk)
            frames.append(data)

        print('녹음 완료!')

        # 스트림 종료
        stream.stop_stream()
        stream.close()
        audio.terminate()

        # WAV 파일로 저장
        wf = wave.open(filepath, 'wb')
        wf.setnchannels(self.channels)
        wf.setsampwidth(audio.get_sample_size(self.format))
        wf.setframerate(self.rate)
        wf.writeframes(b''.join(frames))
        wf.close()

        print(f'파일 저장: {filepath}')
        return filepath

    def list_recordings(self):
        '''녹음 파일 목록 반환'''
        wav_files = sorted(Path(self.records_dir).glob('*.wav'))
        return [str(f) for f in wav_files]

    def speech_to_text(self, audio_file, language='ko-KR'):
        '''
        음성 파일을 텍스트로 변환

        Args:
            audio_file (str): 음성 파일 경로
            language (str): 인식 언어

        Returns:
            list: [(시간, 텍스트)] 형태의 리스트
        '''
        print(f'\nSTT 처리 중: {audio_file}')

        results = []

        try:
            with sr.AudioFile(audio_file) as source:
                # 전체 오디오 길이 계산
                audio_duration = source.DURATION

                # 5초 단위로 분할하여 인식
                segment_duration = 5
                offset = 0

                while offset < audio_duration:
                    # 오디오 세그먼트 읽기
                    audio_data = self.recognizer.record(
                        source,
                        duration=min(segment_duration, audio_duration - offset),
                        offset=offset
                    )

                    try:
                        # Google Speech Recognition 사용
                        text = self.recognizer.recognize_google(
                            audio_data,
                            language=language
                        )

                        # 시간 포맷: MM:SS
                        time_str = f'{int(offset // 60):02d}:{int(offset % 60):02d}'
                        results.append((time_str, text))
                        print(f'  [{time_str}] {text}')

                    except sr.UnknownValueError:
                        print(f'  [{int(offset // 60):02d}:{int(offset % 60):02d}] (인식 불가)')
                    except sr.RequestError as e:
                        print(f'  API 오류: {e}')

                    offset += segment_duration

        except Exception as e:
            print(f'오류 발생: {e}')

        return results

    def save_to_csv(self, audio_file, stt_results):
        '''
        STT 결과를 CSV 파일로 저장

        Args:
            audio_file (str): 음성 파일 경로
            stt_results (list): STT 결과 리스트
        '''
        # CSV 파일명 생성
        csv_file = audio_file.replace('.wav', '.csv')

        with open(csv_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['시간', '인식된 텍스트'])
            writer.writerows(stt_results)

        print(f'CSV 저장 완료: {csv_file}')

    def process_audio_file(self, audio_file, language='ko-KR'):
        '''음성 파일 처리 (STT + CSV 저장)'''
        stt_results = self.speech_to_text(audio_file, language)
        if stt_results:
            self.save_to_csv(audio_file, stt_results)
        return stt_results

    def process_all_recordings(self, language='ko-KR'):
        '''모든 녹음 파일 처리'''
        recordings = self.list_recordings()

        if not recordings:
            print('녹음 파일이 없습니다.')
            return

        print(f'\n총 {len(recordings)}개의 녹음 파일 처리 시작...')

        for audio_file in recordings:
            # CSV 파일이 이미 존재하면 스킵
            csv_file = audio_file.replace('.wav', '.csv')
            if os.path.exists(csv_file):
                print(f'이미 처리됨: {audio_file}')
                continue

            self.process_audio_file(audio_file, language)

    # 보너스 1: 날짜 범위 검색
    def search_by_date_range(self, start_date, end_date):
        '''
        날짜 범위로 녹음 파일 검색

        Args:
            start_date (str): 시작 날짜 (YYYYMMDD)
            end_date (str): 종료 날짜 (YYYYMMDD)

        Returns:
            list: 해당 범위의 파일 목록
        '''
        recordings = self.list_recordings()
        filtered = []

        for file_path in recordings:
            filename = os.path.basename(file_path)
            # YYYYMMDD-HHMMSS.wav 형식에서 날짜 추출
            file_date = filename.split('-')[0]

            if start_date <= file_date <= end_date:
                filtered.append(file_path)

        return filtered

    # 보너스 2: 키워드 검색
    def search_by_keyword(self, keyword):
        '''
        CSV 파일에서 키워드 검색

        Args:
            keyword (str): 검색할 키워드

        Returns:
            list: [(파일명, 시간, 텍스트)] 형태의 검색 결과
        '''
        csv_files = sorted(Path(self.records_dir).glob('*.csv'))
        results = []

        for csv_file in csv_files:
            with open(csv_file, 'r', encoding='utf-8') as f:
                reader = csv.reader(f)
                next(reader)  # 헤더 스킵

                for row in reader:
                    if len(row) >= 2 and keyword in row[1]:
                        results.append((os.path.basename(csv_file), row[0], row[1]))

        return results


def main():
    '''메인 함수'''
    recorder = JavisRecorder()

    while True:
        print('\n' + '=' * 50)
        print('JAVIS - 음성 녹음 및 STT 시스템')
        print('=' * 50)
        print('1. 마이크 목록 보기')
        print('2. 음성 녹음')
        print('3. 녹음 파일 목록')
        print('4. STT 처리 (개별 파일)')
        print('5. STT 처리 (전체 파일)')
        print('6. 날짜 범위 검색')
        print('7. 키워드 검색')
        print('0. 종료')
        print('=' * 50)

        choice = input('선택: ').strip()

        if choice == '1':
            recorder.list_microphones()

        elif choice == '2':
            try:
                duration = int(input('녹음 시간(초, 기본 5초): ') or '5')
                device_input = input('마이크 번호(Enter=기본): ').strip()
                device_index = int(device_input) if device_input else None

                recorder.record_audio(duration, device_index)
            except Exception as e:
                print(f'오류: {e}')

        elif choice == '3':
            recordings = recorder.list_recordings()
            if recordings:
                print(f'\n총 {len(recordings)}개의 녹음 파일:')
                for i, file_path in enumerate(recordings, 1):
                    print(f'{i}. {os.path.basename(file_path)}')
            else:
                print('녹음 파일이 없습니다.')

        elif choice == '4':
            recordings = recorder.list_recordings()
            if not recordings:
                print('녹음 파일이 없습니다.')
                continue

            print('\n녹음 파일 목록:')
            for i, file_path in enumerate(recordings, 1):
                print(f'{i}. {os.path.basename(file_path)}')

            try:
                idx = int(input('처리할 파일 번호: ')) - 1
                if 0 <= idx < len(recordings):
                    language = input('언어 코드(기본 ko-KR): ').strip() or 'ko-KR'
                    recorder.process_audio_file(recordings[idx], language)
                else:
                    print('잘못된 번호입니다.')
            except Exception as e:
                print(f'오류: {e}')

        elif choice == '5':
            language = input('언어 코드(기본 ko-KR): ').strip() or 'ko-KR'
            recorder.process_all_recordings(language)

        elif choice == '6':
            start = input('시작 날짜(YYYYMMDD): ').strip()
            end = input('종료 날짜(YYYYMMDD): ').strip()

            if len(start) == 8 and len(end) == 8:
                results = recorder.search_by_date_range(start, end)
                if results:
                    print(f'\n{len(results)}개의 파일 발견:')
                    for file_path in results:
                        print(f'  - {os.path.basename(file_path)}')
                else:
                    print('해당 기간의 파일이 없습니다.')
            else:
                print('날짜 형식이 잘못되었습니다.')

        elif choice == '7':
            keyword = input('검색할 키워드: ').strip()
            if keyword:
                results = recorder.search_by_keyword(keyword)
                if results:
                    print(f'\n{len(results)}개의 결과 발견:')
                    for filename, time, text in results:
                        print(f'[{filename}] [{time}] {text}')
                else:
                    print('검색 결과가 없습니다.')

        elif choice == '0':
            print('프로그램을 종료합니다.')
            break

        else:
            print('잘못된 선택입니다.')


if __name__ == '__main__':
    main()
