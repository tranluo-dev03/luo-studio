"""Gen 20 ảnh tham chiếu tài xế (phông xanh) cho 20 biến thể canh-sat-gia-su-ai: 10 nam, 10 nữ; Ấn Độ / Mexico / Mỹ.
Muse qua LUO-API của Studio đang chạy. Chỉ đổi người lái xe (HOC); cảnh sát, bé, robot Aiva giữ nguyên.
Chạy:  .venv\\Scripts\\python.exe SAMPLE\\canh-sat-gia-su-ai\\cong-cu\\gen_20_tai_xe.py [01 05 ...]   (bỏ trống = cả 20; ảnh đã có thì bỏ qua, thêm --lai để gen đè)
Ảnh ra: SAMPLE/canh-sat-gia-su-ai/anh/20-tai-xe/tai-xe-XX.png  +  danh-sach.csv"""
import csv, json, os, subprocess, sys, time, uuid, threading
from concurrent.futures import ThreadPoolExecutor
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
sys.path[:0] = [os.path.join(ROOT, "app", "luo-studio"), os.path.join(ROOT, "app", "production")]
import engine as E, gen_video as G  # noqa: E402

OUT = os.path.join(ROOT, "SAMPLE", "canh-sat-gia-su-ai", "anh", "20-tai-xe")
STYLE = ("stylized 3D-animated feature-film look (Pixar-like 3D CARTOON, big expressive eyes, soft rounded features, clean smooth skin shading), "
         "NOT a realistic or semi-realistic face, soft even studio light")
SHEET = ("Character reference picture: ONE person only, shown from the waist up, standing straight and facing the camera in a slight three-quarter front view, "
         "relaxed friendly face, mouth closed, arms relaxed at the sides, on a perfectly flat solid chroma-key GREEN background (pure green screen, #00B140, "
         "even colour, no shadows, no gradient, no floor, no props). No green anywhere on the person or clothes. No text, no logo, no lettering anywhere. Vertical 9:16.")
NEG = "text, letters, logo, watermark, extra people, distorted face, realistic photo, semi-realistic face, green clothing, background objects, gradient background, shadow on background"

# (mã, giới, nước, mô tả tiếng Việt cho bảng duyệt, mô tả gửi Muse)
NV = [
 ("01", "Nam", "Mexico", "Nam Mexico 35t, tóc đen vuốt ngược, ria mép dày, áo sơ mi kẻ caro xanh dương xắn tay",
  "a Mexican man about 35, slicked-back black hair, a thick black moustache, warm brown eyes, tan skin, a blue checked short-sleeved shirt with rolled sleeves, a silver wristwatch"),
 ("02", "Nam", "Mexico", "Nam Mexico 30t, tóc xoăn ngắn, râu quai nón tỉa gọn, áo thun trắng + dây chuyền thánh giá bạc",
  "a Mexican man about 30, short curly dark-brown hair, a neatly trimmed full beard, brown eyes, light-brown skin, a plain white crew-neck T-shirt, a small silver cross necklace"),
 ("03", "Nam", "Mexico", "Nam Mexico 42t, hơi đậm người, tóc húi cua có sợi bạc, áo polo đỏ đô",
  "a stocky Mexican man about 42, a short buzz cut with a few grey hairs, a round friendly face, a short greying goatee, brown skin, a dark-red polo shirt"),
 ("04", "Nam", "Mexico", "Nam Mexico 28t, tóc undercut, đeo kính râm cài trên đầu, áo sơ mi denim",
  "a slim Mexican man about 28, black undercut hairstyle, sunglasses pushed up on his head, clean-shaven, warm brown eyes, tan skin, a light-blue denim button shirt"),
 ("05", "Nam", "India", "Nam Ấn Độ 34t, tóc đen gọn, ria mép, áo sơ mi trắng tay ngắn",
  "an Indian man about 34, neat short black hair with a side part, a thick black moustache, dark-brown eyes, medium-brown skin, a crisp white short-sleeved shirt, a steel kada bracelet"),
 ("06", "Nam", "India", "Nam Ấn Độ (Sikh) 38t, khăn turban xanh navy, râu dài đen, áo sơ mi xám",
  "a Sikh Indian man about 38, a navy-blue turban, a full long black beard, kind dark eyes, medium-brown skin, a light-grey short-sleeved shirt, a steel kada bracelet"),
 ("07", "Nam", "India", "Nam Ấn Độ 29t, tóc dày vuốt lên, râu lún phún, áo kurta ngắn màu vàng nghệ",
  "a young Indian man about 29, thick black hair styled up, light stubble, dark-brown eyes, brown skin, a short mustard-yellow cotton kurta shirt"),
 ("08", "Nam", "US", "Nam Mỹ da trắng 36t, tóc vàng cát, râu ngắn, áo flannel đỏ đen",
  "a white American man about 36, sandy-blond short hair, a short sandy beard, blue eyes, fair lightly freckled skin, a red-and-black flannel shirt over a grey T-shirt"),
 ("09", "Nam", "US", "Nam Mỹ gốc Phi 33t, tóc fade ngắn, râu quai nón tỉa, áo thun xanh navy",
  "an African-American man about 33, a short fade haircut, a neatly trimmed beard, warm dark-brown eyes, deep-brown skin, a fitted navy-blue T-shirt"),
 ("10", "Nam", "US", "Nam Mỹ da trắng 40t, tóc nâu hói nhẹ, đeo kính gọng đen, áo polo xám",
  "a white American man about 40, short brown hair with a slightly receding hairline, black-framed glasses, clean-shaven, hazel eyes, fair skin, a heather-grey polo shirt"),
 ("11", "Nữ", "Mexico", "Nữ Mexico 32t, tóc đen dài gợn sóng, khuyên tròn vàng, áo hai dây cam san hô",
  "a Mexican woman about 32, long wavy black hair, big brown eyes, tan skin, gold hoop earrings, a coral-orange sleeveless top"),
 ("12", "Nữ", "Mexico", "Nữ Mexico 38t, tóc nâu buộc đuôi ngựa, áo blouse thêu hoa trắng",
  "a Mexican woman about 38, brown hair in a high ponytail, warm brown eyes, light-brown skin, a white embroidered peasant blouse with colourful flower embroidery at the neckline"),
 ("13", "Nữ", "Mexico", "Nữ Mexico 28t, tóc bob ngắn đen, son đỏ, áo thun vàng",
  "a young Mexican woman about 28, a short black bob haircut, red lipstick, dark-brown eyes, brown skin, a sunny-yellow T-shirt, small stud earrings"),
 ("14", "Nữ", "India", "Nữ Ấn Độ 33t, tóc đen dài tết một bên, bindi đỏ, áo kurti hồng",
  "an Indian woman about 33, long black hair in a single side braid, a small red bindi, dark expressive eyes, medium-brown skin, a pink cotton kurti top, thin gold bangles"),
 ("15", "Nữ", "India", "Nữ Ấn Độ 40t, tóc búi, khuyên tai vàng to, áo kurti xanh lam (teal)",
  "an Indian woman about 40, black hair in a low bun, large gold jhumka earrings, kind dark eyes, brown skin, a teal cotton kurti top with a small printed border"),
 ("16", "Nữ", "India", "Nữ Ấn Độ 29t, tóc ngang vai uốn nhẹ, đeo kính, áo sơ mi trắng",
  "a young Indian woman about 29, shoulder-length softly curled black hair, thin rounded glasses, dark-brown eyes, light-brown skin, a plain white cotton shirt"),
 ("17", "Nữ", "India", "Nữ Ấn Độ 36t, tóc đen dài thẳng, khuyên mũi nhỏ, áo kurti tím",
  "an Indian woman about 36, long straight black hair over one shoulder, a tiny nose stud, dark eyes, medium-brown skin, a purple kurti top"),
 ("18", "Nữ", "US", "Nữ Mỹ da trắng 34t, tóc vàng ngang vai, áo thun xanh da trời",
  "a white American woman about 34, shoulder-length straight blonde hair, blue eyes, fair skin with light freckles, a sky-blue T-shirt"),
 ("19", "Nữ", "US", "Nữ Mỹ gốc Phi 31t, tóc xoăn tự nhiên buộc cao, khuyên tròn bạc, áo ba lỗ trắng",
  "an African-American woman about 31, natural curly hair in a high puff, silver hoop earrings, warm brown eyes, deep-brown skin, a white tank top"),
 ("20", "Nữ", "US", "Nữ Mỹ da trắng 39t, tóc đỏ nâu búi lỏng, áo sơ mi kẻ caro xanh navy-trắng",
  "a white American woman about 39, auburn hair in a loose messy bun, grey-blue eyes, fair skin, a navy-and-white checked short-sleeved shirt"),
]
# nhân vật phụ cho 20 biến thể: nam cảnh sát (đi với tài xế nữ), bé gái theo nước của tài xế (bé Mexico dùng anh/BE.png có sẵn)
PHU = [
 ("canh-sat-nam", "Nam cảnh sát Mỹ (đi với 10 tài xế nữ)",
  "an American policeman in his early forties, short dark-brown hair, a clean-shaven square jaw, calm kind brown eyes, light-tan skin, a navy short-sleeved police uniform with a plain gold badge and shoulder patches without lettering, a black duty belt with a radio"),
 ("be-an", "Bé gái Ấn Độ 5 tuổi (tài xế Ấn Độ)",
  "an Indian girl about five years old, very big dark-brown eyes, long black hair in two braids tied with small red ribbons, a tiny bindi, brown skin, a pink ruffled sleeveless dress"),
 ("be-trang", "Bé gái Mỹ da trắng 5 tuổi (tài xế Mỹ da trắng)",
  "a white American girl about five years old, very big blue eyes, light-brown hair in two pigtails with colourful clips, light freckles, fair skin, a pink ruffled sleeveless dress"),
 ("be-phi", "Bé gái Mỹ gốc Phi 5 tuổi (tài xế Mỹ gốc Phi)",
  "an African-American girl about five years old, very big brown eyes, natural curly hair in two puffs with colourful bobbles, deep-brown skin, a pink ruffled sleeveless dress"),
]


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    lai = "--lai" in sys.argv
    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, "danh-sach.csv"), "w", encoding="utf-8-sig", newline="") as f:
        w = csv.writer(f)
        w.writerow(["Mã", "Giới", "Nước", "Mô tả", "Ảnh", "Prompt Muse (NGUOI_HOC)"])
        for m, gt, nc, vi, en in NV:
            w.writerow([m, gt, nc, vi, f"tai-xe-{m}.png", en])
        for k, vi, en in PHU:
            w.writerow([k, "", "", vi, f"{k}.png", en])
    tat_ca = [(m, en, f"tai-xe-{m}.png") for m, _, _, _, en in NV] + [(k, en, f"{k}.png") for k, _, en in PHU]
    jobs = [n for n in tat_ca if (not args or n[0] in args) and (lai or not os.path.exists(os.path.join(OUT, n[2])))]
    run = json.load(open(os.path.join(ROOT, "userdata", "running.json"), encoding="utf-8"))
    api = E.Api(f"http://127.0.0.1:{run['api_port']}", G.read_key() or json.load(open(os.path.join(ROOT, "userdata", "studio", "settings.json"), encoding="utf-8")).get("api_key", ""))

    def one(n):
        m, en, ten = n
        sess = f"taixe-{m}-{int(time.time())}-{uuid.uuid4().hex[:5]}"
        prompt = f"{SHEET} {STYLE}. The person: {en}."
        for lan in range(3):
            try:
                print(f"[{m}] gen (lần {lan+1})...", flush=True)
                b = api.generate("image", G.muse_image_prompt(prompt, NEG, 0), [], sess, timeout=600, cancel=threading.Event(), aspect="9:16")
                dst = os.path.join(OUT, ten)
                if b[:4] == b"RIFF":  # Muse trả WebP: đổi sang PNG thật
                    tmp = dst + ".webp"
                    open(tmp, "wb").write(b)
                    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", tmp, dst], check=True)
                    os.remove(tmp)
                else:
                    open(dst, "wb").write(b)
                print(f"[{m}] -> {ten} ({len(b)//1024} KB)", flush=True)
                return
            except Exception as e:  # noqa: BLE001
                print(f"[{m}] lỗi: {e}", flush=True)
        print(f"[{m}] BỎ (3 lần lỗi)", flush=True)

    with ThreadPoolExecutor(4) as ex:
        list(ex.map(one, jobs))

if __name__ == "__main__":
    main()
