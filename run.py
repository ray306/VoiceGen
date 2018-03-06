#!/usr/bin/env python
# -*- coding: utf-8 -*-

# =============================================================================
#  Name：Make_voice
#  Version: 1.5 (Nov 1, 2017)
#  Author: Jinbiao Yang (ray306 at gmail.com)
#
#  Dependencies: numpy, pandas, librosa, jieba, pypinyin [ffmpg]
#  Voice sources：
#     Male：NeoSpeech.Chinese.Liang_v3.11.0.0
#     Female：NeoSpeech.Chinese.Liang_v3.11.0.0
#
# =============================================================================
#  Copyright (c) 2017-. Jinbiao Yang (ray306 at gmail.com).
# =============================================================================

"""
########################################
** USEAGE: 
1. 双击run.bat
2. 输入male -[参数]=[值]或female -[参数]=[值]，然后回车

** Example:
1: 
    male -fn=test.xlsx
        使用男声音源，并指定刺激列表文件为test.xlsx。
2: 
    female -fn=test.xlsx -dt=0.3
        使用女声音源，并指定刺激列表文件为test.xlsx，指定每个拼音发音长0.3秒。

########################################

Parameters：
    -h, or --help 
            show this help message and exit
    -fn, or --filename,
            FILENAME, 默认:'stimuli.xlsx'
                包含刺激列表的excel文件,至少有两列数据。
                第一列是要输出的文件名（列名输入'filename'），第二列是对应的文本（列名输入'text'）
    -dt, or --duration_target,
            DURATION_TARGET 默认:0.25
                每个拼音发音的目标长度（秒）
    -n, or --nature,
            NATURE 默认:0
                是否产生自然发音。选0会固定每个字的发音长度，选1会只固定整个text的发音长度
    -g, or --gender,
            GENDER 默认:'male'
                使用的音源的性别
    -wd, or --weaken_duration,
            WEAKEN_DURATION 默认:0.025
                每个拼音发音的声音结尾的渐弱时间（秒）。
                增加此数值可以减少不同拼音间转换的突兀感，但设置过高会导致发音损失过多信息。
    -o, or --output,
            OUTPUT 默认:'output',
                存放生成的wav文件的文件夹

Notice：
    - 如果路径下只有一个xlsx文件，则使用这个文件作为刺激列表文件
    - 刺激列表文件中支持填入文本（作为单独一列，列名为text），也可以直接填入拼音（作为单独一列，列名为pinyin，声调用0-4表示）
    - 如果刺激列表文件中没有pinyin这一列，程序会先根据text列的内容自动生成pinyin列。
      生成的内容可能有错，所以请做一遍人工检查并修正错误。

"""

import sys
import argparse
import os
import re
import shutil
import urllib.request

path = sys.path[0] # os.getcwd() # 音源路径
# sys.path = [path, path+'/ffmpeg/bin/'] + sys.path

import numpy as np
import pandas as pd

try:
    import librosa
    import jieba
    import pypinyin
    from pypinyin import pinyin, lazy_pinyin
except:
    os.system('conda install -c conda-forge resampy')
    os.system('pip install librosa')
    os.system('pip install jieba')
    os.system('pip install pypinyin')
    import librosa
    import jieba
    import pypinyin
    from pypinyin import pinyin, lazy_pinyin

'拼音转为声音数据（wav）'
def toSound(pinyins, duration_target, nature, gender, weaken_duration):
    def getPinyinWav(gender, py, duration):
        fileloc = f'source/{gender}/00/{py}.wav'

        if not os.path.exists(f'{path}/{fileloc}'):
            urllib.request.urlretrieve("http://cls.ru.nl/~jyang/voice_gen/"+fileloc, filename=f'{path}/{fileloc}')

        # 变速
        os.system(
            f'{path}/tools/Praat.exe --run {path}/tools/change_duration.praat "{py}" "{path}/{fileloc}" "{path}/temp" {duration_target}')
        
        syllable_data, sr = librosa.load(f'{path}/temp/{py}.wav')

        return syllable_data, sr

    sound_data = np.array([])

    if not nature:
        for py in pinyins:
            syllable_data, sr = getPinyinWav(gender, py, duration_target)

            # 截掉
            weaken_sample = int(weaken_duration * sr)
            syllable_data_new = np.concatenate(
                [syllable_data[:-weaken_sample],
                 syllable_data[-weaken_sample:] * np.cos(np.linspace(0, np.pi / 2, weaken_sample))])

            sound_data = np.concatenate([sound_data, syllable_data_new])
    else:
        ##TODO
        pass

    return (sound_data*32767).astype(np.int16)

'汉字转为拼音'
def toPinyin(sentence):
    def reorder(py):
        new = ''
        tone = ''
        for i in py:
            if i in ['1', '2', '3', '4']:
                tone = i
            else:
                new += i
        new += tone
        return new

    sentence = re.sub(r"[。，“”：]", " ", sentence)
    pyList = [reorder(i[0]) for i in pinyin(sentence, style=pypinyin.TONE2)]
    # blank
    for i in range(len(pyList)):
        if ' ' in pyList[i]:
            pyList[i] = ' '
    # sandhi
    for i in range(len(pyList) - 1):
        if pyList[i][-1] == '3' and pyList[i + 1][-1] == '3' and pyList[i] != 'wo3':
            pyList[i] = pyList[i][:-1] + '2'
    # light
    for i in range(len(pyList)):
        if pyList[i] != ' ' and pyList[i][-1] not in ['1', '2', '3', '4']:
            pyList[i] = pyList[i] + '5'
    return pyList

'声音数据输出为wav文件'
def toWavFile(name, pinyins, duration_target, nature, gender, weaken_duration, output):
    
    sound_data = toSound(pinyins, duration_target, nature,
                         gender, weaken_duration)
    librosa.output.write_wav(f'{path}/{output}/{gender}/{name}.wav', sound_data, 22050)
    print(f'{output}/{gender}/{name}.wav')


def processArgs():
    parser = argparse.ArgumentParser(prog=os.path.basename(sys.argv[0]),
                                     formatter_class=argparse.RawDescriptionHelpFormatter,
                                     description=__doc__)

    parser.add_argument("-fn", "--filename", default='stimuli.xlsx',
                        help="包含刺激列表的excel文件,至少有两列数据。\n第一列是要输出的文件名（列名输入'filename'），第二列是对应的文本（列名输入'text'）")
    parser.add_argument("-dt", "--duration_target", default=0.25,
                        help="每个拼音发音的目标长度（秒）")
    parser.add_argument("-n", "--nature", default=0,
                        help="是否产生自然发音。选0会固定每个字的发音长度，选1会只固定整个text的发音长度")
    parser.add_argument("-g", "--gender", default='male',
                        help="使用的音源的性别")
    parser.add_argument("-wd", "--weaken_duration", default=0.025,
                        help="每个拼音发音的声音结尾的渐弱时间（秒）\n加此数值可以减少不同拼音间转换的突兀感，但设置过高会导致发音损失过多信息。")
    parser.add_argument("-o", "--output", default='output',
                        help="存放生成的wav文件的文件夹")

    args = parser.parse_args()
    filename = args.filename
    duration_target = float(args.duration_target)
    nature = int(args.nature)
    gender = args.gender
    weaken_duration = float(args.weaken_duration)
    output = args.output

    fns = [i for i in os.listdir(path) if i[-5:]=='.xlsx']
    if len(fns) == 1:
        filename = fns[0]
    elif filename not in fns: 
        raise Exception('读取文件出错！请检查路径是否正确以及文件内容是否规范。')

    print('本次参数为： \n\
    filename=%s ,\n\
       (加上参数“-fn=XXX”可调整)\n\
    duration_target=%s,\n\
       (加上参数“-dt=XXX”可调整)\n\
    nature=%s,\n\
       (加上参数“-n=XXX”可调整)\n\
    gender=%s,\n\
       (加上参数“-g=XXX”可调整)\n\
    weaken_duration=%s,\n\
       (加上参数“-wd=XXX”可调整)\n\
    output=%s\n\
       (加上参数“-o=XXX”可调整)\n\
    '
        %(filename, duration_target, nature, gender, weaken_duration, output))

    return filename, duration_target, nature, gender, weaken_duration, output

'读取excel文件, 根据text列生成pinyin列，并输出wav'
def main(filename='stimuli.xlsx', duration_target=0.25, gender='male', weaken_duration=0.025, nature=False, output='output'):
    filename, duration_target, nature, gender, weaken_duration, output = processArgs()

    # read excel
    df = pd.read_excel(path+'/'+filename)
    
    if 'filename' not in df.columns: # generate the filenames
        df['filename'] = ["%0*d" % (len(str(len(df))), i+1) for i in range(len(df))]

    if 'pinyin' not in df.columns:
        df['pinyin'] = df['text'].apply(lambda x: ' '.join(toPinyin(x)))
        df.to_excel('%s/%s_new.xlsx' %(path,filename[:-5]), index=None)
        print('请检查新文件%s_new.xlsx中的pinyin列。' % filename[:-5])
    
    # generate WAVs
    input_val = input('\n是否开始生成wav文件?\n  否（直接回车）/ 是（输入y并回车）\n')
    if input_val == 'y':
        if not os.path.exists(f'{path}/temp'):
            os.mkdir(f'{path}/temp')
        if not os.path.exists(f'{path}/{output}'):
            os.mkdir(f'{path}/{output}')
        if not os.path.exists(f'{path}/{output}/{gender}'):
            os.mkdir(f'{path}/{output}/{gender}')

        df.apply(lambda x: toWavFile(
            x.filename, x.pinyin.split(' '),
            duration_target, nature, gender, weaken_duration, output), axis=1)

        shutil.rmtree(f'{path}/temp')

    print('End.')

if __name__ == '__main__':
    main()
