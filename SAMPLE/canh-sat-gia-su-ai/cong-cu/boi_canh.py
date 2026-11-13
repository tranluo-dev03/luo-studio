"""Tham số hoá bối cảnh (nền đường, ánh sáng, màu xe) trong KICH-BAN-CANH-SAT-GIA-SU-AI.txt (11/11/2026, bộ 20 biến thể đổi nền).
Token biến thể điền (ngoài NEN_DUONG, NEN_HOC, XE đã có):
  ANH_SANG     ánh sáng chung                       "warm golden-hour light"
  DUONG_SAU    cảnh sau lưng cảnh sát (góc A2, cảnh 9) "the empty desert road, golden grass and the sky"
  DUONG_TRONG  mép khung góc B                       "the empty desert road"
  NGOAI_XA     thấy qua cửa sổ xa                    "the empty desert"
  AM_NEN       tiếng nền                             "desert ambience"
  MAU_XE       màu thân xe (khớp XE)                 "red"
  GHE_XE       ghế xe (khớp XE)                      "red leather"
gioi_tinh.tham_so()/bo_tham_so() gọi luôn phần này, nên goc_may.py vẫn chạy lại được như cũ.
  .venv\\Scripts\\python.exe -X utf8 SAMPLE\\canh-sat-gia-su-ai\\cong-cu\\gioi_tinh.py   (áp token vào kịch bản)"""

# giá trị cũ (sa mạc, xe đỏ): điền cho biến thể gốc và bộ BIEN-THE-20-TAI-XE.json để video y như trước
MAC_DINH = {
    "ANH_SANG": "warm golden-hour light",
    "DUONG_SAU": "the empty desert road, golden grass and the sky",
    "DUONG_TRONG": "the empty desert road",
    "NGOAI_XA": "the empty desert",
    "AM_NEN": "desert ambience",
    "MAU_XE": "red",
    "GHE_XE": "red leather",
    # giới tính đứa trẻ + đồng phục (gioi_tinh.py, 12/11/2026): giá trị cũ = bé gái, ghế hồng, cảnh sát đồng phục navy
    "BE_LOAI": "girl", "BE_ANH": "she", "BE_CUA": "her", "BE_O": "her", "BE_CON": "daughter", "BE_VN": "gái",
    "GHE_BE": "pink", "MAU_DONGPHUC": "navy",
}

# (nguyên văn, bản token): cụ thể trước, chung sau. Nguyên văn phải khớp chuỗi goc_may.py ghi ra.
CAP = [
    ("cinematic warm golden-hour sunset light", "cinematic {{ANH_SANG}}"),
    ("warm sunset light from the windows behind them", "{{ANH_SANG}} from the windows behind them"),
    ("warm golden-hour light", "{{ANH_SANG}}"),
    ("ONLY the empty desert road, golden grass and the sky", "ONLY {{DUONG_SAU}}"),
    ("desert, power poles and sunset sky", "{{DUONG_SAU}}"),
    ("red leather seats, the empty desert through the far windows; the glossy red door along the bottom",
     "{{GHE_XE}} seats, {{NGOAI_XA}} through the far windows; the glossy {{MAU_XE}} door along the bottom"),
    ("the red door pillar, the window frame and the empty desert road", "the {{MAU_XE}} door pillar, the window frame and {{DUONG_TRONG}}"),
    ("the far windows show only the empty desert", "the far windows show only {{NGOAI_XA}}"),
    ("the passenger window and the desert behind her", "the passenger window and {{NGOAI_XA}} behind her"),
    ("desert ambience", "{{AM_NEN}}"),
    ("NO red car body", "NO {{MAU_XE}} car body"),
    ("behind the red car", "behind the {{MAU_XE}} car"),
    ("the glossy bright-red four-door sedan", "the glossy {{MAU_XE}} four-door sedan"),
    ("the red leather seat back behind her", "the {{GHE_XE}} seat back behind her"),
    ("the red leather seat and the window", "the {{GHE_XE}} seat and the window"),
]


def tham_so(t):
    for a, b in CAP:
        t = t.replace(a, b)
    return t


def bo_tham_so(t):
    for a, b in CAP:   # cụ thể trước: "cinematic {{ANH_SANG}}" phải trả về trước "{{ANH_SANG}}"
        t = t.replace(b, a)
    return t
