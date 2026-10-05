# 条纹学习实验室：从一束条纹，到三维世界

**在线阅读：[https://vg188.github.io/fringe-learning-lab/](https://vg188.github.io/fringe-learning-lab/)**

面向零基础读者的三篇论文学习教程。20课、6个交互实验、逐章小测、学习进度与笔记、可下载的完整 Markdown 讲义。

## 学习内容

1. 像素、正弦、相位、条纹成像与三角测量。
2. N 步相移的公式推导、数值例子、空间与时间展开。
3. 九类相位提取方法、八类误差、十类绝对相位恢复方案及选型。
4. CNN、卷积、训练与 Feng 等人的级联背景／M-D 预测方法。
5. 原版 U-Net 的结构、训练策略、实验结论和回归应用边界。
6. Python 数值实验、名词表、两周学习安排和正文覆盖索引。

本教程是正文主要内容的教学重组，不是逐句翻译或三篇研究的完整代码复现。未核实的独立补充材料细节没有作为事实补写；所有交互实验是明确公式驱动的模拟或结构导览，没有运行训练好的神经网络。

## 阅读与离线使用

- 在线：打开上方 GitHub Pages 地址。
- 离线：下载仓库 ZIP 并完整解压，使用 Chrome／Edge 打开 index.html。
- 讲义：网页顶部“下载讲义”可导出全文，也可直接阅读[完整学习讲义](完整学习讲义.md)。

无需 Node.js、Python、登录或联网即可阅读下载后的网页。脚本、KaTeX 和字体均使用本地相对路径；不是仅下载一个 HTML 就能带走全部资源。本站未提供 Service Worker，不能保证未下载的在线网页断网后仍可访问。

## 学习记录与隐私

进度、答题选择与笔记保存在当前浏览器的 localStorage，应用不会把这些记录上传。切换浏览器、文件路径或网站来源，会使用不同存储；清理浏览器数据可能丢失记录。请使用“导出笔记”保存 Markdown 备份。

网站由 GitHub Pages 提供静态资源，访问请求由托管服务处理；本站无分析统计、广告、后端数据库或远程 AI 调用。

## 来源与图像说明

- Zuo et al. (2018). *Phase shifting algorithms for fringe projection profilometry: A review*. [DOI](https://doi.org/10.1016/j.optlaseng.2018.04.019)
- Feng et al. (2019). *Fringe pattern analysis using deep learning*. [DOI](https://doi.org/10.1117/1.AP.1.2.025001)
- Ronneberger, Fischer, Brox (2015). *U-Net: Convolutional Networks for Biomedical Image Segmentation*. [arXiv v1](https://arxiv.org/abs/1505.04597v1)

公开仓库**不包含论文 PDF、论文原图截图、个人聊天记录、测试笔记或本地日志**。四张 SVG 为本教程绘制的功能／尺寸示意，不是论文插图的直接复制；图中文字注明参考来源与简化范围。KaTeX 0.16.22 的 MIT 许可保留在 [vendor/katex/LICENSE](vendor/katex/LICENSE)。

## 本地修改

网页为原生 HTML/CSS/JavaScript，没有前端构建框架。course.json 是课程正文；build_course.py 生成 lessons.js 与完整讲义。

~~~shell
python -m pip install -r requirements-build.txt
python build_course.py
python validate_site.py
python examples/phase_lab.py
~~~

最后一步仅使用标准库，在 examples 生成实验统计；这些生成文件不会提交。

## 静态托管

GitHub Pages 发布 main 分支的根目录。仓库带有 .nojekyll，不需要 Jekyll、服务端程序或构建密钥。

更新网页时修改并验证后，将源码及生成的 lessons.js／讲义一起提交到 main；GitHub Pages 自动重新发布。
