import requests
import os
import re
from bs4 import BeautifulSoup
from tqdm import tqdm
import time
import copy
import jsonlines as jsl
import csv

letter_num = {'0':'a', '1':'b', '2':'c', '3':'d', '4':'e', '5':'f', '6':'g', '7':'h', '8':'i',
              '9':'j', '10':'k', '11':'l', '12':'m', '13':'n', '14':'o', '15':'p', '16':'q',
              '17':'r', '18':'s', '19':'t', '20':'u', '21':'v', '22':'w', '23':'x', '24':'y', '25':'z'}

def entry_num(target):
    req = requests.get(url=target)
    req.encoding = 'utf-8'
    html = req.text
    bs = BeautifulSoup(html, 'lxml')
    text_entry_number = bs.find('p', class_='entryNumbers')
    if text_entry_number == None:
        return False
    if text_entry_number.text == '':
        return 1
    else:
        entry_number = int(text_entry_number.text[-2])
        return entry_number


def spans(bs, explain):
    spans = bs.find_all('span')
    if spans:
        for span in spans:
            if span['class'] == ['text-uppercase']:
                # $
                if span.text in explain[0][0]:
                    explain[0].remove(explain[0][0])
                explain[0].append('$' + span.text)
            elif span['class'][-3:] == ['t', 'no-aq', 'sents']:
                # example
                explain[1].append(span.text)
            else:
                continue
    return

def detailed_word(item, entry_number, property):
    if property == 'verb':
        if item.p == None:
            dict = {'type': 'verb', 'detailed': []}
        elif item.p.text.strip() == 'transitive':
            dict = {'type': 'transitive verb', 'detailed': []}
        else:
            dict = {'type': item.p.text.strip(), 'detailed': []}
    else:
        dict = {'type': property, 'detailed': []}
    explanations = item.children
    j = 0
    for explanation in explanations:
        if explanation == ' ' or not explanation.div:
            continue
        j += 1
        for explanation_item in explanation.children:
            if explanation_item != ' ':
                word_texts = explanation_item.find_all('span', class_='dtText')
                for n in range(len(word_texts)):
                    word_text = word_texts[n]
                    explain = [[], [], ['Entry' + entry_number, str(j)]]
                    explain[-1].append(letter_num[explanation_item['class'][0].split('-')[-1]])
                    if len(word_texts) > 1:
                        explain[-1].append(str(n + 1))
                    bs5 = BeautifulSoup(str(word_text), 'lxml')
                    explain[0].append(bs5.text.strip(':').split('\n')[0].split(':')[0].strip())
                    spans(bs5, explain)
                    dict['detailed'].append(explain)
    return dict

def detailed_phrase(phrase_name, dict, entry_number):
    bs4 = BeautifulSoup(str(phrase_name), 'lxml')
    phrase_explanations = bs4.find_all('span', class_="dtText")
    j = 0
    for phrase_explanation in phrase_explanations:
        j += 1
        explain = [[], [], ['Entry' + entry_number, str(j)]]
        bs5 = BeautifulSoup(str(phrase_explanation), 'lxml')
        explain[0].append(bs5.text.strip(':').split('\n')[0].split(':')[0].strip())
        spans(bs5, explain)
        dict["explanation"][0]['detailed'].append(explain)
    newword = dict['phrase'].replace(' ', '%20')
    target = 'https://www.merriam-webster.com/dictionary/' + newword
    entry_numbers = entry_num(target)
    req = requests.get(url=target)
    req.encoding = 'utf-8'
    html = req.text
    bs = BeautifulSoup(html, 'lxml')
    headers = bs.find_all('div', class_='row entry-header')
    if headers == []:
        return dict
    #print(headers[0].h1.text)
    if headers[0].h1.text != dict['center word']:
        for i in range(entry_numbers):
            property = headers[i].find('span', class_='fl').text
            entry_number = str(i + 1)
            entry_text = bs.find('div', id='dictionary-entry-' + entry_number)
            items = entry_text.children
            for item in items:
                bs2 = BeautifulSoup(str(item), 'lxml')
                if bs2.find('div', class_='vg'):
                    # word
                    phrase_dict = detailed_word(item, entry_number, property)
                    dict["external_explanation"].append(phrase_dict)
    return dict



if __name__ == '__main__':
    word_cluster = []
    with open('EnWords.csv', encoding="utf8") as csvfile:
        csv_reader = csv.reader(csvfile)  # 使用csv.reader读取csvfile中的文件
        for row in csv_reader:  # 将csv 文件中的数据保存到birth_data中
            word_cluster.append(row[0])
    word_cluster = word_cluster[3727:]
    pre_word = ''
    pre_word2 = ''
    for word in tqdm(word_cluster):
        target = 'https://www.merriam-webster.com/dictionary/' + word
        req = requests.get(url=target)
        if req.url == 'https://www.merriam-webster.com/not-found':
            print(word + ' not found.')
            continue
        entry_numbers = entry_num(target)
        if entry_numbers == False:
            continue
        req.encoding = 'utf-8'
        html = req.text
        bs = BeautifulSoup(html, 'lxml')
        if bs.find('div', id='dictionary-entry-1') == None:
            continue
        headers = bs.find_all('div', class_='row entry-header')
        if headers == []:
            continue
        word = bs.h1.text
        if word == pre_word or word == pre_word2:
            continue
        pre_word2 = pre_word
        pre_word = word
        word_dict = {'word': word, 'explanation': []}
        for i in range(entry_numbers):
            property = headers[i].find('span', class_='fl')
            if property == None:
                property = 'none'
            else:
                property = property.text
            entry_number = str(i + 1)
            entry_text = bs.find('div', id='dictionary-entry-' + entry_number)
            items = entry_text.children
            for item in items:
                bs2 = BeautifulSoup(str(item), 'lxml')
                if bs2.find('div', class_='dro'):
                    #phrase
                    #print('phrase')
                    phrase = bs2.find('div', class_='dro')
                    bs3 = BeautifulSoup(str(phrase), 'lxml')
                    phrases = bs3.div.children
                    for phrase_name in phrases:
                        if phrase_name == ' ':
                            continue
                        elif phrase_name.string and phrase_name.string != '\\': #name
                            #print(phrase_name, phrase_name.span, phrase_name.text)
                            dict = {"phrase" : phrase_name.string, "center word":word, "explanation":[{'type':word_dict['explanation'][-1]['type'], "detailed":[]}], "external_explanation":[]}
                        else:                  #explanation
                            dict = detailed_phrase(phrase_name, dict, entry_number)
                            if dict['explanation'][0]['detailed'] == []:
                                continue
                            with jsl.open('phrase.jsonl', mode='a') as writer:
                                writer.write(dict)
                            #print(dict)

                elif bs2.find('div', class_='vg'):
                    #word
                    #print('word')
                    dict = detailed_word(item, entry_number, property)
                    word_dict['explanation'].append(dict)
                else:
                    continue
        if word_dict['explanation'] == []:
            continue
        with jsl.open('word.jsonl', mode='a') as writer:
            writer.write(word_dict)
        #print(word_dict)












