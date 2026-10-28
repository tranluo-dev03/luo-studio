"""Điểm mốc khuôn mặt bằng mediapipe, dùng chung cho đo miệng và các bước kiểm tra mediapipe.

- mediapipe 0.10.21 (Python 3.11/3.12): FaceMesh cũ (mp.solutions). Các ngưỡng đo miệng trong engine.mouth_check được chỉnh theo nó, nên giữ nguyên.
- mediapipe >= 0.10.30 (bản duy nhất chạy được trên Python 3.13/3.14): mp.solutions đã bị bỏ, dùng FaceLandmarker (API Tasks) với mô hình
  models/face_landmarker.task (float16, Apache-2.0) đi kèm mã nguồn. Cùng số thứ tự điểm mốc (13/14 môi trong, 61/291 khoé miệng), nhưng hay
  mất dấu mặt nghiêng/quay ngang hơn FaceMesh cũ, và với mặt nghiêng bề rộng miệng theo chiều ngang co lại làm độ mở miệng bị phóng to (báo nhầm
  "mấp máy") -> bề rộng miệng tính cả chiều sâu z. Đối chiếu 40 clip thật (độ nhạy thường): 46/80 kết luận giống FaceMesh cũ, 8 lệch
  (3 báo nhầm, 5 bỏ sót), số còn lại một bên không đo được. Tức là trên Python 3.13/3.14 kiểm tra miệng kém tin cậy hơn 3.11/3.12.
"""
import os

MODEL = os.path.join(os.path.dirname(os.path.abspath(__file__)), "models", "face_landmarker.task")


class _Legacy:
    def __init__(self, mp, min_conf):
        self._fm = mp.solutions.face_mesh.FaceMesh(static_image_mode=True, max_num_faces=1, min_detection_confidence=min_conf)

    def find(self, rgb):
        r = self._fm.process(rgb)
        return r.multi_face_landmarks[0].landmark if r.multi_face_landmarks else None

    def mouth_gap(self, rgb):
        lm = self.find(rgb)
        return abs(lm[14].y - lm[13].y) / (abs(lm[291].x - lm[61].x) + 1e-6) if lm else None

    def close(self):
        self._fm.close()


class _Tasks:
    def __init__(self, mp, min_conf):
        from mediapipe.tasks.python import BaseOptions, vision
        with open(MODEL, "rb") as f:  # nạp bằng bytes: mediapipe không mở được đường dẫn có ký tự ngoài ASCII (thư mục tiếng Việt)
            buf = f.read()
        opts = vision.FaceLandmarkerOptions(base_options=BaseOptions(model_asset_buffer=buf), running_mode=vision.RunningMode.IMAGE,
                                            num_faces=1, min_face_detection_confidence=min_conf, min_face_presence_confidence=min_conf)
        self._mp, self._lm = mp, vision.FaceLandmarker.create_from_options(opts)

    def find(self, rgb):
        import numpy as np
        r = self._lm.detect(self._mp.Image(image_format=self._mp.ImageFormat.SRGB, data=np.ascontiguousarray(rgb)))
        return r.face_landmarks[0] if r.face_landmarks else None

    def mouth_gap(self, rgb):
        lm = self.find(rgb)
        return abs(lm[14].y - lm[13].y) / (((lm[291].x - lm[61].x) ** 2 + (lm[291].z - lm[61].z) ** 2) ** 0.5 + 1e-6) if lm else None

    def close(self):
        self._lm.close()


def landmarker(min_conf=0.5):
    """Bộ dò điểm mốc cho ảnh tĩnh, tối đa 1 khuôn mặt. Với ảnh RGB uint8: .find() -> danh sách điểm (toạ độ chuẩn hoá 0-1) hoặc None;
    .mouth_gap() -> độ mở miệng (khoảng hở môi / bề rộng miệng) hoặc None nếu không thấy mặt. Gọi .close() khi xong."""
    import mediapipe as mp
    return (_Legacy if hasattr(mp, "solutions") else _Tasks)(mp, min_conf)


def probe_code():
    """Mã Python cho tiến trình thử riêng (python -I -c ...): nạp mediapipe, chạy nhận diện trên ảnh trống, in 'ok'."""
    here = os.path.dirname(os.path.abspath(__file__))
    return (f"import sys; sys.path.insert(0, {here!r})\n"
            "import numpy as np, face_mesh as F\n"
            "l = F.landmarker(); l.find(np.zeros((96, 96, 3), np.uint8)); l.close(); print('ok')")
