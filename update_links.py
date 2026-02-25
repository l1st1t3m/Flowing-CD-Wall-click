import os
import json

songs_dir = 'songs'
html_path = os.path.join('html', 'index.html')

# 1. 扫描歌曲并提取真实链接
cover_to_link = {}
print(f"正在扫描 '{songs_dir}' 文件夹下的歌曲信息...")
if os.path.exists(songs_dir):
    for filename in os.listdir(songs_dir):
        if filename.endswith('.json'):
            file_path = os.path.join(songs_dir, filename)
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    if 'cover_path' in data and 'song_id' in data:
                        cover_filename = data['cover_path'].split('/')[-1]
                        song_id = data['song_id']
                        song_name = data.get('song_name', '未知歌曲')
                        artist = data.get('artist', '未知歌手')
                        
                        cover_to_link[cover_filename] = {
                            "url": f"https://music.163.com/#/song?id={song_id}",
                            "title": f"🎵 播放: {song_name} - {artist}"
                        }
            except Exception as e:
                pass

# 2. 修改 html/index.html
if not os.path.exists(html_path):
    print(f"❌ 错误：未找到网页文件 '{html_path}'！")
else:
    with open(html_path, 'r', encoding='utf-8') as f:
        html_content = f.read()

    # 3. 替换被还原或未修改的原始链接
    count = 0
    for cover_filename, info in cover_to_link.items():
        old_tag = f'<a href="covers/{cover_filename}">'
        new_tag = f'<a href="{info["url"]}" target="_blank" title="{info["title"]}">'
        if old_tag in html_content:
            html_content = html_content.replace(old_tag, new_tag)
            count += 1

    # 4. 💎 核心魔法：注入破除鼠标限制的 CSS 和超酷悬浮特效
    css_magic = """
<!-- 破解壁纸模式屏蔽的点击事件，并添加悬浮放大特效 -->
<style>
  /* 强制恢复所有的鼠标互动 */
  body, .scroll, .img-box, a, img {
      pointer-events: auto !important;
  }
  
  /* 给每个可点击的专辑添加过渡动画 */
  .img-box a {
      display: inline-block;
      transition: all 0.3s ease !important;
  }
  
  /* 鼠标悬浮时的爆炸特效：稍微放大、置于顶层、加厚重阴影、稍微提亮 */
  .img-box a:hover {
      transform: scale(1.15) !important;
      z-index: 999 !important;
      position: relative;
      box-shadow: 0 15px 25px rgba(0,0,0,0.8);
      filter: brightness(1.1);
  }
</style>
</head>
"""
    # 确保没有重复注入
    if "破解壁纸模式" not in html_content:
        html_content = html_content.replace('</head>', css_magic)
        print("✅ 成功注入：解除鼠标屏蔽 + 悬浮放大特效 CSS！")

    # 5. 写回文件
    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(html_content)

    print(f"🎉 运行完成！如果有新增或被还原的链接，已更新 {count} 个。（如果为0说明链接上次已替换完，重点是注入特效已生效）")
    print("👉 赶紧双击打开你的 html/index.html 测试一下鼠标悬浮的爽快感吧！")