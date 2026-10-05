"""Build the offline lesson bundle and Markdown handout from course.json."""
import json,re,html
from pathlib import Path
import mistune
ROOT=Path(__file__).resolve().parent
course=json.loads((ROOT/'course.json').read_text(encoding='utf-8'))
md=mistune.create_markdown(escape=False,plugins=['table','strikethrough'])
def convert(text):
    tokens=[]
    def protect(m):
        n=len(tokens); tokens.append(m.group()); return f'MATHPLACEHOLDER{n}ENDTOKEN'
    text=re.sub(r'\$\$[\s\S]+?\$\$|\$(?!\$)[^\n$]+?\$',protect,text)
    text=md(text)
    for n,value in enumerate(tokens): text=text.replace(f'MATHPLACEHOLDER{n}ENDTOKEN',html.escape(value))
    return text
handout=['# '+course['title'],'## '+course['subtitle'],'整理日期：2026-10-05。覆盖三篇所依据的正文，教学重组而非逐句翻译。','网页入口：index.html。互动实验仅在网页中可操作；公式与说明在本讲义中完整保留。','## 目录']
for n,c in enumerate(course['chapters'],1): handout.append(f"{n:02}. {c['title']}")
for n,c in enumerate(course['chapters'],1):
    c['html']=convert(c['body'])
    body=re.sub(r'<div class="lab" data-lab="([^"]+)"></div>',lambda m:'> 交互实验：在网页 index.html 中打开本章（'+m.group(1)+'）。',c['body'])
    q=c['quiz']; answer=q['options'][q['answer']]
    handout.extend(['\n---\n',f"# {n:02}. {c['title']}",c['subtitle'],f"原文定位：{c['source']}",body,'## 本章小测',q['q']]+[f'{i+1}. {a}' for i,a in enumerate(q['options'])]+['\n**答案：**'+answer+'。'+q['explanation']])
(ROOT/'lessons.js').write_text('window.COURSE='+json.dumps(course,ensure_ascii=False).replace('</script','<\\/script')+';\n',encoding='utf-8')
(ROOT/'完整学习讲义.md').write_bytes('\n\n'.join(handout).encode('utf-8'))
print(f"Built {len(course['chapters'])} chapters, {sum(len(c['body']) for c in course['chapters'])} content characters.")

with (ROOT/'lessons.js').open('a',encoding='utf-8') as f: f.write('window.HANDOUT='+json.dumps('\n\n'.join(handout),ensure_ascii=False)+';\n')
