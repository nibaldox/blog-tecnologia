#!/usr/bin/env python3
"""
Generador de blog estático para Vercel
"""
import os
import re
from datetime import datetime

def md_to_html(text):
    """Convierte Markdown básico a HTML"""
    lines = text.split('\n')
    html_lines = []
    in_list = False
    
    for line in lines:
        line = line.strip()
        if not line:
            if in_list:
                html_lines.append('</ul>')
                in_list = False
            continue
            
        # Headers
        if line.startswith('### '):
            if in_list:
                html_lines.append('</ul>')
                in_list = False
            html_lines.append(f'<h3>{line[4:]}</h3>')
        elif line.startswith('## '):
            if in_list:
                html_lines.append('</ul>')
                in_list = False
            html_lines.append(f'<h2>{line[3:]}</h2>')
        elif line.startswith('# '):
            if in_list:
                html_lines.append('</ul>')
                in_list = False
            html_lines.append(f'<h1>{line[2:]}</h1>')
        # Lista
        elif line.startswith('- '):
            if not in_list:
                html_lines.append('<ul>')
                in_list = True
            html_lines.append(f'<li>{line[2:]}</li>')
        # Bold
        elif '**' in line:
            if in_list:
                html_lines.append('</ul>')
                in_list = False
            line = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', line)
            html_lines.append(f'<p>{line}</p>')
        # Blockquote
        elif line.startswith('> '):
            if in_list:
                html_lines.append('</ul>')
                in_list = False
            html_lines.append(f'<blockquote>{line[2:]}</blockquote>')
        # Regular paragraph
        else:
            if in_list:
                html_lines.append('</ul>')
                in_list = False
            # Process inline elements
            line = re.sub(r'\[(.*?)\]\((.*?)\)', r'<a href="\2">\1</a>', line)
            line = re.sub(r'`(.*?)`', r'<code>\1</code>', line)
            html_lines.append(f'<p>{line}</p>')
    
    if in_list:
        html_lines.append('</ul>')
    
    return '\n'.join(html_lines)

def parse_frontmatter(content):
    """Extrae el frontmatter del markdown"""
    if content.startswith('---'):
        parts = content.split('---', 2)
        if len(parts) >= 3:
            fm = parts[1]
            body = parts[2].strip()
            
            data = {}
            for line in fm.strip().split('\n'):
                if ':' in line:
                    key, val = line.split(':', 1)
                    data[key.strip()] = val.strip()
            
            return data, body
    return {}, content

def generate_blog():
    """Genera el blog estático"""
    posts_dir = '/a0/usr/workdir/blog/content/posts'
    output_dir = '/a0/usr/workdir/blog/public'
    
    os.makedirs(output_dir, exist_ok=True)
    
    posts = []
    
    for root, dirs, files in os.walk(posts_dir):
        for f in files:
            if f.endswith('.md'):
                filepath = os.path.join(root, f)
                
                with open(filepath, 'r', encoding='utf-8') as file:
                    content = file.read()
                
                data, body = parse_frontmatter(content)
                
                title = data.get('title', 'Sin título')
                date = data.get('date', datetime.now().strftime('%Y-%m-%d'))
                author = data.get('author', 'Agent Zero')
                tags_str = data.get('tags', '')
                
                tags_html = ''
                if tags_str:
                    tags = tags_str.strip('[]').split(',')
                    for tag in tags:
                        tags_html += f'<span class="tag">{tag.strip()}</span>'
                
                # Generar HTML
                html_content = f'''<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title} | Tech Diario</title>
    <style>
        :root {{
            --primary: #2563eb;
            --bg: #ffffff;
            --text: #1f2937;
            --gray: #6b7280;
        }}
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            line-height: 1.8;
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
            background: var(--bg);
            color: var(--text);
        }}
        header {{
            border-bottom: 2px solid var(--primary);
            padding-bottom: 20px;
            margin-bottom: 40px;
        }}
        h1 {{ color: var(--primary); font-size: 2em; }}
        h2 {{ margin-top: 40px; color: var(--primary); }}
        .meta {{
            color: var(--gray);
            font-size: 0.9em;
        }}
        .tags {{
            display: flex;
            gap: 10px;
            margin: 10px 0;
        }}
        .tag {{
            background: #e5e7eb;
            padding: 4px 12px;
            border-radius: 20px;
            font-size: 0.8em;
        }}
        a {{ color: var(--primary); }}
        pre {{
            background: #1f2937;
            color: #e5e7eb;
            padding: 20px;
            border-radius: 8px;
            overflow-x: auto;
        }}
        blockquote {{
            border-left: 4px solid var(--primary);
            margin: 20px 0;
            padding-left: 20px;
            font-style: italic;
            color: var(--gray);
        }}
        footer {{
            margin-top: 60px;
            padding-top: 20px;
            border-top: 1px solid #e5e7eb;
            text-align: center;
            color: var(--gray);
        }}
    </style>
</head>
<body>
    <header>
        <h1><a href="/index.html" style="text-decoration: none; color: inherit;">📡 Tech Diario</a></h1>
        <p>Noticias diarias de IA, Tecnología e Innovación</p>
    </header>
    
    <article>
        <h1>{title}</h1>
        <div class="meta">📅 {date} | 👤 {author}</div>
        <div class="tags">{tags_html}</div>
        <hr>
        {md_to_html(body)}
    </article>
    
    <footer>
        <p>© 2026 Tech Diario - Generado automáticamente por Agent Zero</p>
    </footer>
</body>
</html>'''
                
                # Guardar archivo HTML
                slug = f.replace('.md', '.html')
                output_path = os.path.join(output_dir, slug)
                with open(output_path, 'w', encoding='utf-8') as f:
                    f.write(html_content)
                
                posts.append({
                    'title': title,
                    'date': date,
                    'file': slug,
                    'excerpt': body[:200] + '...' if len(body) > 200 else body
                })
    
    # Ordenar posts por fecha
    posts.sort(key=lambda x: x['date'], reverse=True)
    
    # Generar índice
    posts_html = ''
    for p in posts:
        posts_html += f'''
        <div class="post">
            <h2><a href="{p['file']}">{p['title']}</a></h2>
            <div class="meta">📅 {p['date']}</div>
            <p class="excerpt">{p['excerpt']}</p>
            <a href="{p['file']}" class="read-more">Leer más →</a>
        </div>
        '''
    
    index = f'''<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Tech Diario - Noticias de IA y Tecnología</title>
    <style>
        :root {{
            --primary: #2563eb;
            --bg: #ffffff;
            --text: #1f2937;
            --gray: #6b7280;
        }}
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            line-height: 1.8;
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
            background: var(--bg);
            color: var(--text);
        }}
        header {{
            border-bottom: 2px solid var(--primary);
            padding-bottom: 20px;
            margin-bottom: 40px;
        }}
        h1 {{ color: var(--primary); }}
        .post {{ margin-bottom: 40px; }}
        .post h2 a {{
            text-decoration: none;
            color: var(--text);
        }}
        .post h2 a:hover {{ color: var(--primary); }}
        .meta {{
            color: var(--gray);
            font-size: 0.9em;
        }}
        .excerpt {{
            margin-top: 10px;
        }}
        .read-more {{
            color: var(--primary);
            text-decoration: none;
            font-weight: bold;
        }}
        footer {{
            margin-top: 60px;
            padding-top: 20px;
            border-top: 1px solid #e5e7eb;
            text-align: center;
            color: var(--gray);
        }}
    </style>
</head>
<body>
    <header>
        <h1>📡 Tech Diario</h1>
        <p>Noticias diarias de IA, Tecnología e Innovación</p>
    </header>
    
    <main>
        {posts_html}
    </main>
    
    <footer>
        <p>© 2026 Tech Diario - Generado automáticamente por Agent Zero</p>
    </footer>
</body>
</html>'''
    
    with open(os.path.join(output_dir, 'index.html'), 'w', encoding='utf-8') as f:
        f.write(index)
    
    print(f"✅ Blog generado: {len(posts)} artículos")
    return posts

if __name__ == '__main__':
    generate_blog()
