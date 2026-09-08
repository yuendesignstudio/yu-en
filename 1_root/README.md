# YU-EN Design Studio ／ Karan Products

公開URL：https://yuendesignstudio.github.io/yu-en/

- ルート（`/`）… YU-EN Design Studio（作品一覧）
- `karan-products/` … Karan Products

## 更新のしかた

作品の文章 → `_data/works.json` を直して `python3 _tools/build_works.py`
作品の写真 → `images/works/<作品>/` に `hero.jpg` `01.jpg` … を入れて同じコマンド
Karanの商品 → `karan-products/_data/items.json` と `karan-products/_tools/build_items.py`

くわしくは、手元の `website/yu-en/README.md` を見てください。
