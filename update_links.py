import os
import json

songs_dir = 'songs'
html_path = os.path.join('html', 'index.html')

# 1. 提取歌曲链接
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

if not os.path.exists(html_path):
    print(f"❌ 错误：未找到网页文件 '{html_path}'！")
else:
    with open(html_path, 'r', encoding='utf-8') as f:
        html_content = f.read()

    # 2. 批量替换：同时给 img 加上 decoding="async" 和 loading="lazy"
    count = 0
    for cover_filename, info in cover_to_link.items():
        old_tag = f'<a href="covers/{cover_filename}">'
        new_tag = f'<a href="{info["url"]}" target="_blank" title="{info["title"]}">'
        
        # 替换 A 标签
        if old_tag in html_content:
            html_content = html_content.replace(old_tag, new_tag)
            count += 1
            
    # 全局替换 img 标签，加入异步解码和原生占位
    html_content = html_content.replace('<img alt="unknown"', '<img alt="unknown" decoding="async" loading="lazy"')

    # 3. 注入【终极破壁版】的超强 CSS
    css_magic = """
<!-- 性能优化与交互特效 -->
<style>
  /* --- 终极核心修复：粉碎所有遮挡与边界裁切 --- */
  
  /* 基础状态：强制允许图片突破上下边界 */
  .img-box, .img-box div {
      position: relative !important;
      z-index: 1 !important;
      overflow: visible !important; /* ★ 极其重要：解除原CSS可能存在的裁切 */
  }

  /* 第1级：只要这排有海报被鼠标悬停，整排立刻置顶防上下遮挡 */
  .img-box:hover,
  .img-box:has(a:hover) {
      z-index: 999 !important;
  }
  
  /* 第2级：所在的滚动半场置顶，防前后遮挡 */
  .img-box div:hover,
  .img-box div:has(a:hover) {
      z-index: 9999 !important;
  }
  /* ----------------------------------------------------------- */

  /* 恢复交互，限定在图片容器上以节省性能 */
  .img-box a {
      pointer-events: auto !important;
      display: inline-block;
      
      /* 优化1：绝对不使用 all，只针对变化属性做动画 */
      transition: transform 0.25s cubic-bezier(0.25, 0.46, 0.45, 0.94), filter 0.25s ease, box-shadow 0.25s ease !important;
      
      /* 优化2：开启 GPU 硬件加速 */
      will-change: transform;
      -webkit-backface-visibility: hidden;
      backface-visibility: hidden;
      transform: translateZ(0); 
  }
  
  .img-box a:hover {
      /* 悬浮时放大 */
      transform: scale(1.15) translateZ(0) !important;
      
      /* 第3级：当前图片自身拥有最高优先级，防左右遮挡 */
      z-index: 99999 !important;
      position: relative !important;
      
      box-shadow: 0 20px 30px rgba(0,0,0,0.6) !important;
      filter: brightness(1.15) !important;
  }

  /* 优化3：解决初始加载白屏时的排版塌陷问题 */
  .img-box img {
      background-color: #2a2a2a; /* 骨架屏深灰占位 */
      min-width: 160px;
      min-height: 160px;
      object-fit: cover;
  }
</style>
</head>
"""
    if "性能优化与交互特效" not in html_content:
        html_content = html_content.replace('</head>', css_magic)

    # 4. 写回文件
    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(html_content)

    print(f"🎉 成功优化并替换了 {count} 首歌曲。上下左右全方位防遮挡已生效！")