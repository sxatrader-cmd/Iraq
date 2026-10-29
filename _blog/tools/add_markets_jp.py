#!/usr/bin/env python3
"""Japan landing pages (Oct 2026): /ja/iraq-tours-from-japan/ (copy of the Japanese homepage)
and /en/iraq-tours-from-japan/ (copy of the English homepage), built with add_markets.build()
plus a travel-advice note pointing to Japan's MOFA overseas-safety site. Not linked from the
homepages. Idempotent:  python3 _blog/tools/add_markets_jp.py
(No South Korea page: South Korea bans its citizens from travelling to Iraq.)"""
import re, pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import add_markets as A

A.UI["ja"] = ("{c}からお越しの方へ", "{c}発 イラク旅行", "{c}からイラクへの行き方", "主な見どころ", "プログラムを見る ↓")
A.VISA["ja"] = ("イラクのビザ", "日本国籍の方は、イラク政府の公式電子ビザポータル（evisa.iq）で事前にオンライン申請できます。クルディスタン地域も対象です。手数料と有効期間は申請時にポータルに表示されます。条件は変わることがあるため、ご予約前に必ずポータルまたはイラク大使館で最新情報をご確認ください。")

A.M.clear()
A.market("japan", "iraq-tours-from-japan", "ja", {"ja": "日本", "en": "Japan"}, {
 "ja": dict(
   title="日本発 イラク旅行：バビロン・ウル・湿地帯をプライベートで | Fable Tour",
   desc="日本からのイラク旅行。東京・大阪から乗り継ぎ1回でバグダッドへ。バビロン、ウル、メソポタミア湿地帯、サーマッラーを専用車とガイドで巡る7日間・9日間ツアー、1名$2,500から。",
   kw="イラク旅行, イラク ツアー 日本発, バビロン遺跡 ツアー, イラク 観光, メソポタミア 旅行, ウル ジッグラト, イラク 電子ビザ 日本人, 東京 バグダッド 航空券, Fable Tour",
   h1="日本発 イラク旅行",
   lead="バビロン、ウル、湿地帯、サーマッラー、ハトラ — 4★〜5★ホテルと専用ガイド付きの2つのプログラム。1名$2,500から。",
   intro="ご希望の日程で、ご家族やご友人だけのプライベート旅行を手配します。空港でお出迎えし、到着から出発まで専用車とガイドがご一緒します。少人数グループへの参加も可能です。",
   travel="日本からイラクへの直行便はありません。東京（成田・羽田）や大阪（関西）から、ドーハ（カタール航空）、ドバイ（エミレーツ航空）、アブダビ（エティハド航空）、イスタンブール（ターキッシュ エアラインズ）で1回乗り継ぎ、バグダッド、バスラ、エルビルへ向かうのが一般的です（最新の運航スケジュールをご確認ください）。日本との時差は6時間（イラクが6時間遅れ）。現地通貨はイラク・ディナールで、日本円の両替は難しいため米ドル現金をお持ちください。ガイドは英語でご案内します。",
   hl=[("babylon", "バビロン", "イシュタル門、行列道路、ネブカドネザルの南宮殿、そして「バビロンのライオン」。"),
       ("ur", "ウルとウルク", "4000年以上前に建てられたウルのジッグラトと、文字が生まれた都市ウルク。"),
       ("marshes", "メソポタミア湿地帯", "世界遺産の湿地帯を伝統の小舟マシューフで巡り、葦の家ムディーフを訪ねます。")]),
 "en": dict(
   title="Iraq Tours from Japan: Flights from Tokyo & Osaka, E-visa | Fable Tour",
   desc="Iraq tours for travellers from Japan: one-stop flights from Tokyo and Osaka, e-visa for Japanese passports, Babylon, Ur, the Marshes and Samarra. Private 7 & 9-day tours from $2,500.",
   kw="Iraq tours from Japan, Iraq tour Japanese travellers, Tokyo to Baghdad, Osaka to Baghdad, Iraq e-visa Japan, Babylon tour, Mesopotamia tour, Fable Tour",
   h1="Iraq tours from Japan",
   lead="Babylon, Ur, the Marshes, Samarra and Hatra — two programmes with 4★–5★ hotels and a private guide, from US$2,500.",
   intro="We arrange a private trip for you, your family or friends on the date you choose, with an airport welcome and a private car and guide from arrival to departure — or join a small group.",
   travel="There are no direct flights from Japan to Iraq. From Tokyo (Narita, Haneda) or Osaka (Kansai), the usual routes are one stop via Doha (Qatar Airways), Dubai (Emirates), Abu Dhabi (Etihad) or Istanbul (Turkish Airlines) to Baghdad, Basra or Erbil (check current schedules). Iraq is six hours behind Japan. Bring US dollars in cash — Japanese yen is hard to exchange in Iraq. Tours are guided in English.",
   hl=[("babylon", "Babylon", "The Ishtar Gate, the Processional Way, Nebuchadnezzar's Southern Palace and the Lion of Babylon."),
       ("ur", "Ur & Uruk", "The ziggurat of Ur, over 4,000 years old, and Uruk, where writing began."),
       ("marshes", "The Marshes", "A mashoof boat ride through the UNESCO-listed Marshes and a visit to a mudhif reed house.")])})

ADVICE = {
 "ja": '<div class="market-info" id="travel-advice" style="margin-top:16px;padding:12px 14px;background:rgba(217,192,142,.18);border-radius:6px;border-left:3px solid var(--gold,#C9A96A)"><p><strong>外務省 海外安全情報</strong> ご旅行を決める前に、<a href="https://www.anzen.mofa.go.jp/" target="_blank" rel="noopener">外務省 海外安全ホームページ</a>でイラクの最新の危険情報を必ずご確認ください。また、海外旅行保険が渡航先をカバーしているかもご確認ください。私たちは現地ガイドによるプライベートツアーを運営しており、政府の勧告に反して渡航を勧めることはありません。</p></div>',
 "en": '<div class="market-info" id="travel-advice" style="margin-top:16px;padding:12px 14px;background:rgba(217,192,142,.18);border-radius:6px;border-left:3px solid var(--gold,#C9A96A)"><p><strong>Japanese government travel advice.</strong> Please read the latest safety information for Iraq on the <a href="https://www.anzen.mofa.go.jp/" target="_blank" rel="noopener">MOFA overseas safety website</a> before you decide, and confirm that your travel insurance covers the destination. We run private programmes with local guides and do not pressure anyone to travel against their government’s advice.</p></div>',
}


def run():
    urls = []
    for key, mk in A.M.items():
        pair = [(mk["local"], A.url(key, mk["local"])), ("en", A.url(key, "en")), ("x-default", A.url(key, "en"))]
        for lang in (mk["local"], "en"):
            u = A.build(key, lang)
            f = A.ROOT / lang / mk["slug"] / "index.html"
            s = f.read_text()
            s = re.sub(r'\s*<div class="market-info" id="travel-advice".*?</div>', "", s, flags=re.S)
            i = s.index("</section>", s.index('class="block in market-panel"'))
            s = s[:i] + "    " + ADVICE[lang] + "\n  " + s[i:]
            f.write_text(s)
            urls.append((u, pair))
    A.sitemap(urls)
    print("built", len(urls), "pages")


if __name__ == "__main__":
    run()
