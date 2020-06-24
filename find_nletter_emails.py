import pickle
from email.parser import HeaderParser
from collections import defaultdict
from tqdm import tqdm
import datetime
import imaplib

with open('./state', 'rb') as f:
    all_mapping = pickle.load(f)
    nletter_mapping = pickle.load(f)

parser = HeaderParser()
reverse_mapping = defaultdict(tuple)

def get_email(inp):
    return inp.split(' ')[-1]

for key in nletter_mapping.keys():
    msg = all_mapping[key][1].decode()
    h = parser.parsestr(msg)
    from_email = h['From']
    reverse_mapping[get_email(from_email)[1:-1]] += (key,)

temp = [(len(reverse_mapping[k]), k) for k in reverse_mapping.keys()]

for t in sorted(temp, reverse=True):
    print(t[0], t[1])

mail = imaplib.IMAP4_SSL('imap.mail.yahoo.com', port=993)
mail.login('', '')
mail.select('inbox')

spam_keys = list(nletter_mapping.keys())

# for key in spam_keys:
#     msg = all_mapping[key][1].decode()
#     h = parser.parsestr(msg)

#     try:
#         d = datetime.datetime.strptime(h['Date'][:24], "%a, %d %b %Y %H:%M:%S")
#     except Exception as ex:
#         erred.append(h['Date'])
#         continue
#     if d > datetime.datetime(year=2020, month=1, day=1):
#         showoff.append(key)


for i in tqdm(range(0, len(spam_keys), 100)):
    keys = spam_keys[i: i+100]
    # r, d = mail.uid('COPY', ','.join(keys).encode(), 'tspam')
    r2, d2 = mail.uid('STORE', ','.join(keys).encode(), '+FLAGS', '(\\Deleted)')
    # if r == 'OK':
    #     r2, d2 = mail.uid('STORE', ','.join(keys).encode(), '+FLAGS', '(\Deleted)')
mail.expunge()
mail.close()
