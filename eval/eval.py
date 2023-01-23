import numpy as np
import sys
import json

def read_resultlog(filename):
    f = open(filename, "r")
    resultlog = f.readlines()
    SER = float(resultlog[1].split(" ")[1])
    test_num = int((len(resultlog) - 11) / 5)
    result = list()
    gt = list()
    pre = list()
    for i in range(test_num):
        result.append(resultlog[11 + i * 5 + 1])
        gt.append(resultlog[11 + i * 5 + 2])
        pre.append(resultlog[11 + i * 5 + 4])
    return SER, result, gt, pre

def parse_to_json(result_string):
    result_now = result_string[:result_string.find('}]}')+3]
    result_now = result_now.replace("<eps>","")
    result_now = ''.join(result_now)
    result_now = result_now.split(" ; ")
    result_now = ''.join(result_now)
    result_now = result_now.replace("|", ",")
    result_now = result_now.replace("\'", "\"")
    result_now = result_now.replace(" ", "")
    result_json = json.loads(result_now)
    return result_json

def eval_TER(result, gt, pre, command_type=None):
    num_sen = 0
    acc_sen = 0
    if (command_type != None):
        command_type = command_type.split(" ")
    for i in range(len(result)):
        result_now = result[i].split(" ")
        wer = float(result_now[2])
        gt_json = parse_to_json(gt[i])
        pre_json = parse_to_json(pre[i])

        if (command_type == None):
            num_sen += 1
            if (gt_json['action'] == pre_json['action']):
                acc_sen += 1
        elif (len(command_type) == 1):
            if (gt_json['action'] == command_type[0]):
                num_sen += 1
                if (gt_json['action'] == pre_json['action']):
                    acc_sen += 1
        else:
            if (gt_json['action'] == command_type[0] and gt_json['entities'][0]['type'] == command_type[1]):
                num_sen += 1
                if (gt_json['action'] == pre_json['action']):
                    acc_sen += 1
    return (1 - acc_sen * 1.0 / num_sen)

def eval_SER(result, gt, pre, command_type=None):
    num_sen = 0
    acc_sen = 0
    if (command_type != None):
        command_type = command_type.split(" ")
    for i in range(len(result)):
        result_now = result[i].split(" ")
        wer = float(result_now[2])
        gt_json = parse_to_json(gt[i])
        pre_json = parse_to_json(pre[i])

        if (command_type == None):
            num_sen += 1
            if (gt_json == pre_json):
                acc_sen += 1
        elif (len(command_type) == 1):
            if (gt_json['action'] == command_type[0]):
                num_sen += 1
                if (gt_json == pre_json):
                    acc_sen += 1
        else:
            if (gt_json['action'] == command_type[0] and gt_json['entities'][0]['type'] == command_type[1]):
                num_sen += 1
                if (gt_json == pre_json):
                    acc_sen += 1
    return (1 - acc_sen * 1.0 / num_sen)

def eval_SEER(result, gt, pre, command_type=None):
    num_entity = 0
    acc_entity = 0
    if (command_type != None):
        command_type = command_type.split(" ")
    for i in range(len(result)):
        result_now = result[i].split(" ")
        wer = float(result_now[2])
        gt_json = parse_to_json(gt[i])
        pre_json = parse_to_json(pre[i])

        if (command_type == None):
            num_entity += 1
            if (gt_json['action'] == pre_json['action']):
                acc_entity += 1
            num_entity += len(gt_json['entities'])
            # print(len(gt_json['entities']))
            for i in range(len(gt_json['entities'])):
                # print(gt_json['entities'][i])
                if (i<len(pre_json['entities'])):
                    if (gt_json['entities'][i] == pre_json['entities'][i]):
                        acc_entity += 1
        elif (len(command_type) == 1):
            if (gt_json['action'] == command_type[0]):
                num_entity += 1
                if (gt_json['action'] == pre_json['action']):
                    acc_entity += 1
                num_entity += len(gt_json['entities'])
                # print(len(gt_json['entities']))
                for i in range(len(gt_json['entities'])):
                    # print(gt_json['entities'][i])
                    if (i<len(pre_json['entities'])):
                        if (gt_json['entities'][i] == pre_json['entities'][i]):
                            acc_entity += 1
        else:
            if (gt_json['action'] == command_type[0] and gt_json['entities'][0]['type'] == command_type[1]):
                num_entity += 1
                if (gt_json['action'] == pre_json['action']):
                    acc_entity += 1
                num_entity += len(gt_json['entities'])
                # print(len(gt_json['entities']))
                for i in range(len(gt_json['entities'])):
                    # print(gt_json['entities'][i])
                    if (i<len(pre_json['entities'])):
                        if (gt_json['entities'][i] == pre_json['entities'][i]):
                            acc_entity += 1
    
    return (1 - acc_entity * 1.0 / num_entity)

if __name__ == "__main__":
    SER, result, gt, pre = read_resultlog(sys.argv[1])
    print("Overall SER: " + str(SER))

    command_type_list = ['weather', 'navigation', 'reminder todo', 'reminder time', 'stock', 'time', 'sun', 'air']

    acc_TER = eval_TER(result, gt, pre)
    print("Overall TER:" + str(acc_TER))

    for command_type in command_type_list:
        acc_TER = eval_TER(result, gt, pre, command_type)
        print(command_type + " TER: " + str(acc_TER))

    acc_SER = eval_SER(result, gt, pre)
    print("Overall SER:" + str(acc_SER))

    for command_type in command_type_list:
        acc_SER = eval_SER(result, gt, pre, command_type)
        print(command_type + " SER: " + str(acc_SER))
    
    acc_SEER = eval_SEER(result, gt, pre)
    print("Overall SEER:" + str(acc_SEER))

    for command_type in command_type_list:
        acc_SEER = eval_SEER(result, gt, pre, command_type)
        print(command_type + " SEER: " + str(acc_SEER))