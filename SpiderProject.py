import requests
import urllib3
from bs4 import BeautifulSoup
import pandas as pd

urllib3.disable_warnings()

url = "https://github.com/trending"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/120.0 Safari/537.36"
}

resp = requests.get(url, headers=headers, verify=False)
print("状态码:", resp.status_code)

soup = BeautifulSoup(resp.text, "html.parser")
articles = soup.select("article.Box-row")
print("找到项目数:", len(articles))

data = []
for a in articles:
    name_tag = a.select_one("h2 a")
    if name_tag is None:
        continue
    name = name_tag.get_text(strip=True).replace("\n", "").replace(" ", "")
    
    star_tag = a.select_one('a[href$="/stargazers"]')
    stars = star_tag.get_text(strip=True) if star_tag else "0"
    
    data.append({"name": name, "stars": stars})

df = pd.DataFrame(data)
df.to_csv("trending.csv", index=False, encoding="utf-8-sig")
print("已保存 trending.csv，共", len(df), "条")
import matplotlib.pyplot as plt

# 中文显示
plt.rcParams["font.sans-serif"] = ["SimHei"]
plt.rcParams["axes.unicode_minus"] = False

# 把 "25,730" 这种带逗号的字符串转成整数
df["stars_num"] = df["stars"].str.replace(",", "").astype(int)

# 按星数从高到低排序，取前10
df_sorted = df.sort_values("stars_num", ascending=False).head(10)

plt.figure(figsize=(12, 6))
plt.barh(df_sorted["name"], df_sorted["stars_num"], color="steelblue")
plt.xlabel("Stars")
plt.title("GitHub Trending Top 10 (by Stars)")
plt.gca().invert_yaxis()  # 星数最多的放最上面
plt.tight_layout()
plt.savefig("chart.png", dpi=150)
plt.show()