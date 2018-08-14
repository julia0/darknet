# plot iterations vs. training loss

import os
from os import path as osp
import matplotlib.pyplot as plt

def extract_lines(file):
    # get line with loss information. write to new file and return said file. 
    new_file = open(osp.join(os.getcwd(), 'lines.txt'), 'w+')
    count = 0
    
    # for graph
    x = []
    y = []
    with open(file) as f:
        iter_num = 0
        for line in f:
            line = line.strip()
            if line.find('00:') != -1:
                if line.find('Saving weights') == -1:
                    new_file.write(line + '\n')
                    count += 1
                    
                    iter_end = line.find(':')
                    iter_section = line[0:line.find(':')]
                    cumm_loss_end = line.find(',')
                    cumm_loss = line[iter_end + 2: cumm_loss_end]
                    avg_loss_end = line.find(' avg loss,')
                    avg_loss = line[cumm_loss_end + 1: avg_loss_end]
                    rate_end = line.find(' rate,')
                    rate = line[avg_loss_end + 10 + 1:rate_end]
                    seconds_end = line.find(' seconds,')
                    seconds = line[rate_end + 6 + 1: seconds_end]
                    images_end = line.find(' images')
                    images = line[seconds_end + 9 + 1:images_end]
                    
                    if float(iter_section) > iter_num:
                        iter_num = float(iter_section)
                        x.append(float(iter_section))
                        y.append(float(cumm_loss))
                        #print(*x, sep='\n')
                        #print(*y, sep='\n')
                        writer.writerow([iter_section, cumm_loss, avg_loss, rate, seconds, images])
        
        
    plt.plot(x,y, label='Loss')
    plt.xlabel('Iteration #')
    plt.ylabel('Loss')
    plt.title('Iterations vs. Loss')
    plt.legend()
    plt.show()
    # print(count)

def main():
    # main
    file_path = 'PATH_TO_LOG_TXT'
    extract_lines(file_path)

if __name__ == '__main__':
    main()
    

