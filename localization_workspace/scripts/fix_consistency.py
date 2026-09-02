# -*- coding: utf-8 -*-
import csv

CANON = {
    "그랑데님...": "المولاة غراندي…",
    "상점": "المتجر",
    "반리온의 문": "بوّابة ڤانريون",
    "기억의 파편": "شظيّة الذاكرة",
    "역병의 핵": "نواة الطاعون",
    "역병의 문양석": "حجر رمز الطاعون",
    "검은 촉수": "اللوامس السوداء",
    "임프리티오 플로라...": "إمبريتيو فلورا…",
    "임프리티오 플로라…": "إمبريتيو فلورا…",
    "5월 1일\n오늘 처음으로 초음파로 모습을 봤어.\n아직 작지만, 거기 있다는 게 느껴졌어.\n나는 하얗고, 아빠":
        "1 مايو\nرأيتُك اليوم للمرّة الأولى عبر الموجات فوق الصوتية.\nما زلتَ صغيرًا جدًّا، لكنّني شعرتُ بوجودك هناك.\nفروي أبيض، ووالدك أسود…\nلمن ستشبه أكثر؟",
    "블루리본 방위대복": "زيّ حرس الشريط الأزرق",
    "청린도포": "رداء الحراشف الزرقاء",
    "홍염난무": "رقصة اللهيب القرمزي",
    "몽령차": "شاي الطيف الحالم",
    "늑대의 문": "بوّابة الذئب",
    "반격의 신호": "إشارة الهجوم المضادّ",
    "엘러드성 깊숙한 곳을 조사해 주게. 봉인 해제에 [왕의 권능]이 필요하다면, 그 단서도 그곳에 있을 걸세.":
        "تحرَّ في أعماق قلعة إلورد. إن كان فكّ الختم يحتاج إلى [سلطان الملك]، فلا بدّ أنّ الدليل هناك أيضًا.",
    "아이사르의 돌 조각을 수집해 제 연구를 도와주세요. 그에 걸맞은 보답은 약속드리겠습니다.":
        "ساعدني في بحثي عبر جمع شظايا حجر آيساري. وأعدك بمكافأة تليق بجهدك.",
    "소르족의 용맹한 전사의 복식을 본떠 만든 옷이란다. 제작에 쓰이는 특별한 옷감만 구할 수 있다면, 언젠가 다시 만들어줄 수 있을 텐데.":
        "ثوبٌ صُنع على غرار زيّ محاربي قبيلة السور الشجعان. لو أمكن الحصول على القماش الخاصّ المستخدَم في صنعه، لربّما أمكن إعادة صنعه يومًا ما.",
    "스카일이 이끄는 블루리본 방위대는 서광의 마을의 든든한 버팀목이지. 대원이 되고 싶으면 스카일에게 이야기해 보렴.":
        "حرس الشريط الأزرق الذي يقوده سكايل ركيزة راسخة لقرية الفجر. إن أردتَ الانضمام إليهم، فتحدّث إلى سكايل.",
    "서광의 마을에 들르게 된다면 내 의상실을 찾아오렴. 네게 꼭 보답을 하고 싶구나.":
        "إن مررتَ يومًا بقرية الفجر، تعالَ إلى محلّ أزيائي. أودّ حقًّا أن أردّ لك الجميل.",
    "작업실 안쪽에 있는 작은 액자 하나만 가져다주면 된단다. 벽에 걸려있어서 금방 찾을 수 있을 게야.":
        "كلّ ما عليك فعله هو إحضار إطار صغير للصور من داخل الورشة. إنّه معلَّق على الجدار فلن يفوتك.",
}

def main():
    rows = list(csv.DictReader(open("10_arabic_translation.csv", encoding="utf-8-sig", newline="")))
    changed = 0
    unmatched = dict(CANON)
    for r in rows:
        src = r["source"]
        if src in CANON:
            if r["target"] != CANON[src]:
                r["target"] = CANON[src]
                changed += 1
            unmatched.pop(src, None)
    with open("10_arabic_translation.csv", "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        w.writerow(["key", "source", "target"])
        for r in rows:
            w.writerow([r["key"], r["source"], r["target"]])
    print(f"changed {changed} rows")
    if unmatched:
        print("WARNING - these canon sources never matched any row:")
        for k in unmatched:
            print(" ", repr(k[:50]))

    # sync into 10_arabic_translation.jsonl too
    import json
    jrows = [json.loads(l) for l in open("10_arabic_translation.jsonl", encoding="utf-8")]
    by_key = {r["key"]: r["target"] for r in csv.DictReader(open("10_arabic_translation.csv", encoding="utf-8-sig"))}
    for jr in jrows:
        if jr["id"] in by_key:
            jr["arabic"] = by_key[jr["id"]]
    with open("10_arabic_translation.jsonl", "w", encoding="utf-8") as f:
        for jr in jrows:
            f.write(json.dumps(jr, ensure_ascii=False) + "\n")
    print("synced jsonl")

if __name__ == "__main__":
    main()
