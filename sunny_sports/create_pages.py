#!/usr/bin/env python3
#-*-coding=utf-8-*-

import mapping
import os

m = mapping.PAGE_MAPPING

PATH = "./templates/"
for url, html in m.items():
    if os.path.isfile(PATH+html):
        continue
    if len(html.split("/")) > 1:
        if not os.path.isdir(PATH+html.split("/")[0]):
            os.mkdir(PATH+html.split("/")[0])
    
    s = "<body><div><h1>%s</h1></div></body>"%html
    with open(PATH+html, "w") as f:
        f.write(s)

