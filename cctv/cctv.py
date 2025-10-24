#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
cctv.py - CCTV 이미지 뷰어 및 사람 감지 시스템 (YOLOv8)

기능:
1. CCTV 이미지 폴더에서 이미지 로드
2. 방향키로 이미지 탐색 (왼쪽/오른쪽)
3. YOLOv8을 이용한 사람 감지
4. 감지된 사람 영역 표시 (빨간색 사각형)
'''

import os
import zipfile
import cv2
from pathlib import Path
from ultralytics import YOLO


class MasImageHelper:
    '''이미지 처리 헬퍼 클래스'''

    def __init__(self, folder_path):
        '''
        초기화 함수

        Args:
            folder_path (str): 이미지 폴더 경로
        '''
        self.folder_path = folder_path
        self.image_files = []
        self.current_index = 0
        self.image_extensions = {'.jpg', '.jpeg', '.png', '.bmp', '.gif'}

        # YOLOv8 모델 로드 (사전 학습된 모델)
        print('YOLOv8 모델 로드 중...')
        self.model = YOLO('yolov8n.pt')  # nano 모델 (빠름)
        print('모델 로드 완료!')

        # 이미지 파일 목록 로드
        self.load_image_list()

    def load_image_list(self):
        '''이미지 파일 목록 로드 (이미지 형식만 필터링)'''
        if not os.path.exists(self.folder_path):
            print(f'폴더가 존재하지 않습니다: {self.folder_path}')
            return

        all_files = sorted(Path(self.folder_path).iterdir())

        for file_path in all_files:
            if file_path.is_file():
                if file_path.suffix.lower() in self.image_extensions:
                    self.image_files.append(str(file_path))

        print(f'총 {len(self.image_files)}개의 이미지 파일 발견')

    def get_image_count(self):
        '''이미지 파일 개수 반환'''
        return len(self.image_files)

    def get_current_image_path(self):
        '''현재 이미지 경로 반환'''
        if 0 <= self.current_index < len(self.image_files):
            return self.image_files[self.current_index]
        return None

    def load_current_image(self):
        '''현재 인덱스의 이미지 로드'''
        image_path = self.get_current_image_path()
        if image_path:
            return cv2.imread(image_path)
        return None

    def next_image(self):
        '''다음 이미지로 이동'''
        if self.current_index < len(self.image_files) - 1:
            self.current_index += 1
            return True
        return False

    def previous_image(self):
        '''이전 이미지로 이동'''
        if self.current_index > 0:
            self.current_index -= 1
            return True
        return False

    def detect_people(self, image):
        '''
        YOLOv8로 이미지에서 사람 감지

        Args:
            image: OpenCV 이미지

        Returns:
            list: [(x, y, w, h, confidence)] 형태의 감지된 사람 영역 목록
        '''
        if image is None:
            return []

        # YOLOv8 추론
        results = self.model(image, verbose=False)

        people = []
        for result in results:
            boxes = result.boxes
            for box in boxes:
                # 클래스 0 = 사람 (COCO dataset)
                if int(box.cls[0]) == 0:
                    # xyxy 형식을 xywh로 변환
                    x1, y1, x2, y2 = box.xyxy[0].cpu().numpy()
                    x = int(x1)
                    y = int(y1)
                    w = int(x2 - x1)
                    h = int(y2 - y1)
                    confidence = float(box.conf[0])

                    # 신뢰도 임계값 (0.5 이상만)
                    if confidence > 0.5:
                        people.append((x, y, w, h, confidence))

        return people

    def draw_people_boxes(self, image, people):
        '''
        감지된 사람 영역에 빨간 사각형 그리기

        Args:
            image: OpenCV 이미지
            people: [(x, y, w, h, confidence)] 형태의 영역 목록

        Returns:
            image: 사각형이 그려진 이미지
        '''
        result = image.copy()

        for detection in people:
            x, y, w, h = detection[:4]
            confidence = detection[4] if len(detection) > 4 else 0

            # 빨간색 사각형 그리기
            cv2.rectangle(result, (x, y), (x + w, y + h), (0, 0, 255), 2)

            # 텍스트 추가 (신뢰도 포함)
            label = f'Person {confidence:.2f}'
            cv2.putText(
                result,
                label,
                (x, y - 10),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.5,
                (0, 0, 255),
                2
            )

        return result

    def show_image(self, image, window_name='CCTV 이미지'):
        '''
        이미지 화면에 표시

        Args:
            image: OpenCV 이미지
            window_name: 윈도우 이름
        '''
        if image is not None:
            cv2.imshow(window_name, image)


def extract_cctv_zip(zip_path, extract_path):
    '''
    CCTV.zip 파일 압축 해제

    Args:
        zip_path (str): zip 파일 경로
        extract_path (str): 압축 해제 경로
    '''
    if os.path.exists(zip_path):
        print(f'압축 해제 중: {zip_path}')
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(extract_path)
        print(f'압축 해제 완료: {extract_path}')
    else:
        print(f'zip 파일이 없습니다: {zip_path}')


def image_viewer_mode(helper):
    '''
    이미지 뷰어 모드 (방향키로 탐색)

    Args:
        helper: MasImageHelper 인스턴스
    '''
    print('\n=== 이미지 뷰어 모드 ===')
    print('왼쪽 방향키: 이전 이미지')
    print('오른쪽 방향키: 다음 이미지')
    print('ESC: 종료')
    print('=' * 50)

    window_name = 'CCTV 이미지 뷰어'

    while True:
        # 현재 이미지 로드
        image = helper.load_current_image()

        if image is None:
            print('이미지를 로드할 수 없습니다.')
            break

        # 현재 정보 표시
        current_path = helper.get_current_image_path()
        filename = os.path.basename(current_path)
        info_text = f'[{helper.current_index + 1}/{helper.get_image_count()}] {filename}'

        # 텍스트를 이미지에 추가
        display_image = image.copy()
        cv2.putText(
            display_image,
            info_text,
            (10, 30),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0, 255, 0),
            2
        )

        # 이미지 표시
        helper.show_image(display_image, window_name)

        # 키 입력 대기
        key = cv2.waitKey(0) & 0xFF

        if key == 27:  # ESC
            break
        elif key == 83 or key == 3:  # 오른쪽 방향키
            if not helper.next_image():
                print('마지막 이미지입니다.')
        elif key == 81 or key == 2:  # 왼쪽 방향키
            if not helper.previous_image():
                print('첫 번째 이미지입니다.')

    cv2.destroyAllWindows()


def people_detection_mode(helper):
    '''
    사람 감지 모드 (자동 검색)

    Args:
        helper: MasImageHelper 인스턴스
    '''
    print('\n=== 사람 감지 모드 (YOLOv8) ===')
    print('사람이 감지된 이미지만 표시합니다.')
    print('Enter: 다음 검색')
    print('ESC: 종료')
    print('=' * 50)

    window_name = 'CCTV 사람 감지'
    helper.current_index = 0
    found_count = 0
    total_people = 0

    while helper.current_index < helper.get_image_count():
        # 현재 이미지 로드
        image = helper.load_current_image()
        current_path = helper.get_current_image_path()
        filename = os.path.basename(current_path)

        print(f'\n검색 중: [{helper.current_index + 1}/{helper.get_image_count()}] {filename}')

        if image is None:
            print('  이미지 로드 실패')
            helper.next_image()
            continue

        # 사람 감지
        people = helper.detect_people(image)

        if len(people) > 0:
            found_count += 1
            total_people += len(people)
            print(f'  ✓ {len(people)}명의 사람 감지!')

            # 사각형 그리기
            result_image = helper.draw_people_boxes(image, people)

            # 정보 텍스트 추가
            info_text = f'[{helper.current_index + 1}/{helper.get_image_count()}] {filename} - {len(people)}명'
            cv2.putText(
                result_image,
                info_text,
                (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (0, 255, 0),
                2
            )

            # 이미지 표시
            helper.show_image(result_image, window_name)

            # 키 입력 대기
            key = cv2.waitKey(0) & 0xFF

            if key == 27:  # ESC
                print('\n검색을 중단합니다.')
                break
            elif key == 13 or key == 10:  # Enter
                helper.next_image()
        else:
            print('  사람 없음')
            helper.next_image()

    # 검색 완료
    if helper.current_index >= helper.get_image_count():
        print('\n검색이 완료되었습니다!')
        print(f'총 {found_count}개의 이미지에서 {total_people}명의 사람을 찾았습니다.')

    cv2.destroyAllWindows()


def main():
    '''메인 함수'''
    print('=' * 50)
    print('CCTV 이미지 뷰어 및 사람 감지 시스템 (YOLOv8)')
    print('=' * 50)

    # CCTV 폴더 경로
    cctv_folder = './CCTV'

    # CCTV.zip이 있으면 압축 해제
    zip_path = './CCTV.zip'
    if os.path.exists(zip_path) and not os.path.exists(cctv_folder):
        extract_cctv_zip(zip_path, './')

    # 현재 디렉토리에 이미지가 있으면 사용
    if not os.path.exists(cctv_folder):
        cctv_folder = '.'

    # MasImageHelper 초기화
    helper = MasImageHelper(cctv_folder)

    if helper.get_image_count() == 0:
        print('이미지 파일을 찾을 수 없습니다.')
        return

    # 메뉴
    while True:
        print('\n' + '=' * 50)
        print('1. 이미지 뷰어 모드 (방향키로 탐색)')
        print('2. 사람 감지 모드 (YOLOv8 자동 검색)')
        print('0. 종료')
        print('=' * 50)

        choice = input('선택: ').strip()

        if choice == '1':
            image_viewer_mode(helper)
        elif choice == '2':
            people_detection_mode(helper)
        elif choice == '0':
            print('프로그램을 종료합니다.')
            break
        else:
            print('잘못된 선택입니다.')


if __name__ == '__main__':
    main()
