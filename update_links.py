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
        
        if old_tag in html_content:
            html_content = html_content.replace(old_tag, new_tag)
            count += 1
            
    html_content = html_content.replace('<img alt="unknown"', '<img alt="unknown" decoding="async" loading="lazy"')

    # 3. 注入【终极破壁版 + 悬停不暂停】的超强 CSS
    css_magic = """
<!-- 性能优化与交互特效 -->
<style>
  /* --- 终极核心修复：粉碎所有遮挡与边界裁切 --- */
  .img-box, .img-box div {
      position: relative !important;
      z-index: 1 !important;
      overflow: visible !important;
  }

  /* ★ 强制覆盖原生 CSS：无论鼠标怎么放，绝对不允许暂停原生动画！ */
  .img-box:hover, 
  .img-box:hover div,
  .img-box:hover a {
      animation-play-state: running !important;
  }

  .img-box:hover, .img-box:has(a:hover) { z-index: 999 !important; }
  .img-box div:hover, .img-box div:has(a:hover) { z-index: 9999 !important; }

  /* 拖拽时全局鼠标指针变化 */
  .img-box { cursor: grab; }
  body.is-grabbing, body.is-grabbing * { cursor: grabbing !important; }

  /* 恢复交互，限定在图片容器上以节省性能 */
  .img-box a {
      pointer-events: auto !important;
      display: inline-block;
      transition: transform 0.25s cubic-bezier(0.25, 0.46, 0.45, 0.94), filter 0.25s ease, box-shadow 0.25s ease !important;
      will-change: transform;
      -webkit-backface-visibility: hidden;
      backface-visibility: hidden;
      transform: translateZ(0); 
  }
  
  .img-box a:hover {
      transform: scale(1.15) translateZ(0) !important;
      z-index: 99999 !important;
      position: relative !important;
      box-shadow: 0 20px 30px rgba(0,0,0,0.6) !important;
      filter: brightness(1.15) !important;
  }

  /* 骨架屏深灰占位 */
  .img-box img {
      background-color: #2a2a2a; 
      min-width: 160px;
      min-height: 160px;
      object-fit: cover;
  }
</style>
</head>
"""
    if "性能优化与交互特效" not in html_content:
        html_content = html_content.replace('</head>', css_magic)

    # 4. 注入【不停流淌版 滚轮/拖拽 JS】
    js_magic = """
<!-- 全局联动拖拽与滚轮互交脚本 (自然流淌版) -->
<script>
document.addEventListener("DOMContentLoaded", () => {
    const allAnimElements = document.querySelectorAll('.img-box, .img-box div');
    
    let isDown = false;
    let isDragging = false;
    let isVertical = null;
    let startX = 0, startY = 0, lastX = 0;
    
    const pauseAll = () => {
        allAnimElements.forEach(el => el.getAnimations().forEach(anim => anim.pause()));
    };
    
    const playAll = () => {
        allAnimElements.forEach(el => el.getAnimations().forEach(anim => anim.play()));
    };
    
    // 核心黑科技：直接拨动运行中的动画时间线，实现“快进/倒退”
    const scrub = (delta) => {
        allAnimElements.forEach(el => {
            el.getAnimations().forEach(anim => {
                anim.currentTime += delta * 15; 
            });
        });
    };

    const start = (e) => {
        if (!e.target.closest('.img-box')) return;
        
        isDown = true;
        isDragging = false;
        isVertical = null;
        startX = e.type.includes('mouse') ? e.pageX : e.touches[0].pageX;
        startY = e.type.includes('mouse') ? e.pageY : e.touches[0].pageY;
        lastX = startX;
        
        document.body.classList.add('is-grabbing');
        pauseAll(); // 仅在按住鼠标拖拽时暂停（为了不跟手起冲突）
    };

    const move = (e) => {
        if (!isDown) return;
        
        const currentX = e.type.includes('mouse') ? e.pageX : e.touches[0].pageX;
        const currentY = e.type.includes('mouse') ? e.pageY : e.touches[0].pageY;
        
        if (isVertical === null) {
            if (Math.abs(currentY - startY) > Math.abs(currentX - startX) + 5) {
                isVertical = true; 
            } else if (Math.abs(currentX - startX) > 5) {
                isVertical = false; 
                isDragging = true;
            }
        }
        
        if (isVertical === true) return; 
        
        if (isVertical === false && e.cancelable) {
            e.preventDefault(); 
        }
        
        const deltaX = lastX - currentX;
        lastX = currentX;
        scrub(deltaX * 2.5); 
    };

    const end = () => {
        if (!isDown) return;
        isDown = false;
        document.body.classList.remove('is-grabbing');
        playAll(); // 鼠标一松开，立刻恢复自然滚动！
    };

    window.addEventListener('mousedown', start);
    window.addEventListener('mousemove', move, { passive: false });
    window.addEventListener('mouseup', end);
    
    window.addEventListener('touchstart', start, { passive: true });
    window.addEventListener('touchmove', move, { passive: false });
    window.addEventListener('touchend', end);
    
    // ★ 滚轮与触控板逻辑：不需要暂停，直接叠加时间线
    window.addEventListener('wheel', (e) => {
        if (Math.abs(e.deltaY) > Math.abs(e.deltaX) + 10 && e.deltaX === 0) return;
        if (e.cancelable) e.preventDefault();
        
        const delta = Math.abs(e.deltaX) > Math.abs(e.deltaY) ? e.deltaX : e.deltaY;
        scrub(delta * 4); // 画面依然在自动播放，这里只是额外叠加了一股力推着它走
    }, { passive: false });

    // 防误触：拖拽结束后阻断链接跳转
    window.addEventListener('click', (e) => {
        if (isDragging && e.target.closest('a')) {
            e.preventDefault();
            e.stopPropagation();
        }
    }, { capture: true });
    
    // ★ 已经彻底删除了原版代码中鼠标悬停 (mouseenter) 带来的暂停效果！
});
</script>
</body>
"""
    if "全局联动拖拽与滚轮互交脚本" not in html_content:
        html_content = html_content.replace('</body>', js_magic)


    # 5. 写回文件
    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(html_content)

    print(f"🎉 交互升级成功！")