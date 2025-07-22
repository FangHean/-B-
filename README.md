# 爬取B站动态关键词并绘制词云图
## 实现方法：
- 通过访问B站动态的api获得某个用户的动态文本内容，过滤无关内容，通过jieba分词，输出词云图。
## 示例：
- 打开`extraction_from_bilibili(moments).py`，将`headers`中的`cookie`换成自己的cookie
  <img width="373" height="191" alt="image" src="https://github.com/user-attachments/assets/e9a05303-74aa-42da-80c0-258cc6421769" />
- 运行`extraction_from_bilibili(moments).py`，输入要爬取的用户uid，得到`bilibili_text.txt`
  <img width="327" height="104" alt="image" src="https://github.com/user-attachments/assets/5f889afe-9de2-4e8c-aec7-e41222dc6c1c" />
- 打开`draw.py`，将`png = Image.open("J0Lu.png")`替换为本地图片路径（透明背景），此处用洛天依GSC#1424粘土人的官方人设图（画师：Tid）作为示例：
  <img width="1000" height="1000" alt="J0Lu" src="https://github.com/user-attachments/assets/b90a180d-4659-4770-996b-085b9040f05a" />
  <img width="1000" height="1000" alt="ciyuntu" src="https://github.com/user-attachments/assets/ee666cbf-de18-4d03-9e6c-ede74e7c1aad" />
