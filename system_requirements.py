import matplotlib.pyplot as plt
import re

def GPU_relation(df):
    gpuinfo = df[['owners', 'GPU']][df['GPU'] != '']
    gpu_sn = {'': (0, 0)}

    def parse_spec(x):
        x = str(x)
        gpu_info = re.search(r'\d+', x, re.IGNORECASE)
        if gpu_info is not None:
            sn = int(gpu_info.group())
            if sn < 100 or sn > 3000:  # invalid data
                return ''
            elif sn > 2999:  # old nvidia card
                gpu_sn[f'NVIDIA GeForce {sn}'] = (0, 0)
                return f'NVIDIA GeForce {sn}'
            else:
                gpu_sn[f' {sn}'] = (sn // 100, sn % 100)
                if sn % 100 == 0:
                    return ''
                return f' {sn}'
        return ''

    gpuinfo['GPU Info'] = gpuinfo['GPU'].apply(parse_spec)
    grouped_info = gpuinfo[gpuinfo['GPU Info'] != ''][['GPU Info', 'owners']].groupby('GPU Info').sum().sort_values(by='owners', ascending=False)[:30]
    grouped_info = grouped_info.reset_index()
    grouped_info['sn'] = grouped_info['GPU Info'].apply(lambda x: gpu_sn[x][0])
    grouped_info['sn2'] = grouped_info['GPU Info'].apply(lambda x: gpu_sn[x][1])
    grouped_info = grouped_info.sort_values(by=['sn2', 'sn'])

    colors = ['C0', 'C1', 'C2', 'C3', 'C4', 'C5', 'C6', 'C7', 'C8', 'C9']
    color_list = []
    color_index = 0
    last_sn = grouped_info['sn2'][0]
    for index, curr_sn in enumerate(grouped_info['sn2']):
        if curr_sn != last_sn:
            color_index = color_index + 1
            last_sn = curr_sn
        if color_index >= len(colors):
            color_index = 0
        color_list.append(colors[color_index])

    plt.figure(figsize=(10, 7))
    ax = plt.barh(grouped_info['GPU Info'], grouped_info['owners'], color=color_list)
    plt.xticks(fontsize=14)
    plt.yticks(fontsize=14)
    plt.xlabel('Recommended Graphics Card (NVIDIA GTX)', fontsize=20)
    plt.ylabel('Owners', fontsize=20)
    plt.title('Graphics Card Requirements vs Owners', fontsize=26)
    lg = plt.legend(handles=[ax[1:8], ax[9:17], ax[17:23], ax[24:30]], labels=['Low', 'Medium', 'High', 'Very High'], title='Tier', fontsize=14,
                    fancybox=True, shadow=True)
    lg.get_title().set_fontsize(16)
    plt.tight_layout()
    plt.show()
