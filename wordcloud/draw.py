from matplotlib import pyplot as plt
import jieba
from PIL import Image
import numpy as np
from wordcloud import WordCloud, ImageColorGenerator

# 读文本
text = open("bilibili_text.txt", "rt", encoding="utf-8").read()

# 停用词
base_stop = {
    "的","了","在","是","我","你","他","她","它","这","那","和","就","都","而","及","与","或",
    "也","一个","我们","你们","他们","她们","自己","啊","哦","嗯","吧","呢","嘛","又","非常"
}
# 继续追加B站常见废话
extra_stop = {"抽奖","转发","点赞","关注","评论","收藏","投币","互动","私信","小伙伴","来啦","上线","链接","详情","查看","官方","支持","粉丝","洛天","出洛天","预售","详情","恭喜","通知","详情","点击","请点击","天猫","旗舰店","请点击","网页","链接","会员","时间","所有","系列","周边","随机","产品","信息","产品信息","详情请"}
stopwords = base_stop | extra_stop

# jieba
words = [w for w in jieba.lcut(text) if w.strip() and w not in stopwords and len(w) > 1]
seg_text = " ".join(words)

png = Image.open("J0Lu.png")
# 取 alpha 通道，如果没有就转成 L 灰度
if png.mode == "RGBA":
    mask_arr = np.array(png.split()[-1])      # alpha 通道
else:
    mask_arr = np.array(png.convert("L"))

# 让白色区域填字：把非透明(>0)设为255，透明(=0)设为0
mask_arr = np.where(mask_arr>0, 255, 0).astype(np.uint8)
mask_arr = 255 - mask_arr

color_arr = np.array(png.convert("RGB"))
# 读灰度图用于形状遮罩

wc = WordCloud(
    font_path="SourceHanSansSC-Regular.otf",
    background_color="white",
    mask = mask_arr,
    color_func=ImageColorGenerator(color_arr)
).generate(seg_text)

wc.to_file("ciyuntu.png")
plt.imshow(wc, interpolation="bilinear")
plt.axis("off")
plt.show()