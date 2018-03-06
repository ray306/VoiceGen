########################################
* USEAGE: 
1. 双击run.bat
2. 输入male -[参数]=[值]或female -[参数]=[值]，然后回车

* Example:
1: 
    male -fn=test.xlsx
        使用男声音源，并指定刺激列表文件为test.xlsx。
2: 
    female -fn=test.xlsx -dt=0.3
        使用女声音源，并指定刺激列表文件为test.xlsx，指定每个拼音发音长0.3秒。

########################################

* Parameters：
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
                增加此数值可以减少声音结尾突兀感，但设置过高会导致发音损失过多信息。
    -o, or --output,
            OUTPUT 默认:'output',
                存放生成的wav文件的文件夹

* Notice：
    - 如果路径下只有一个xlsx文件，则使用这个文件作为刺激列表文件
    - 刺激列表文件中支持填入文本（作为单独一列，列名为text），也可以直接填入拼音（作为单独一列，列名为pinyin，声调用0-4表示）
    - 如果刺激列表文件中没有pinyin这一列，程序会先根据text列的内容自动生成pinyin列。
      生成的内容可能有错，所以请做一遍人工检查并修正错误。