"""
Python script to connect to your account via imap and systematically detect all newsletters
"""

import pickle
from email.parser import HeaderParser
import imaplib
from tqdm import tqdm
mail = imaplib.IMAP4_SSL('imap.mail.yahoo.com', port=993)
mail.login('', '')      # <---------------------------------------------- Edit this
t = mail.list()
# Out: list of "folders" aka labels in gmail.
mail.select("inbox")  # connect to inbox.

# result, data = mail.search(None, "ALL")
result, data = mail.uid('search', None, 'ALL')

ids = data[0]  # data is a list.
id_list = [x.decode() for x in ids.split()]  # ids is a space separated string

all_mapping = dict()
nletter_mapping = dict()

parser = HeaderParser()

DIFF = 200

for i in tqdm(range(0, len(id_list), DIFF)):
    uids = id_list[i: i+DIFF]
    r, d = mail.uid('fetch', ','.join(id_list[i:i+DIFF]), '(UID BODY.PEEK[HEADER])')
    if result != 'OK':
        print(i, 'to', i+DIFF, result)
        continue
    for k, uid in zip(range(0, len(d), 2), uids):
        all_mapping[uid] = d[k]
        h = parser.parsestr(d[k][1].decode("UTF-8"))
        if 'List-Unsubscribe' in h.keys():
            nletter_mapping[uid] = d    

with open('./state', 'wb') as f:
    pickle.dump(all_mapping, f)
    pickle.dump(nletter_mapping, f)

print("Dump all data")
