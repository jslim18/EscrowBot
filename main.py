import StringIO
import cStringIO
import json
import logging
import random
import urllib
import urllib2

# for sending images
from PIL import Image
import multipart

# standard app engine imports
from google.appengine.api import urlfetch
from google.appengine.ext import ndb
import webapp2

TOKEN = '99219372009:AAESU3DbmKgKjgkp0jeZ-Y3yQBbmcawHsNc99'

BASE_URL = 'https://api.telegram.org/bot' + TOKEN + '/'

MYBOTNAME = '@EscrowBot'
#DEAL = '0'

ANS01 = 'EscrowBot is a name you can trust, managed and insured by Escrow Team. EscrowBot is owned by Crypto*Trade 2.0'
ANS02 = '32EyQiKfmqAz8AA5PcabUVbUsxSxWVif6w'
ANS03 = 'Every trade made through escrow is protected by insurance up to 0.50 BTC per transaction in case it went burst'
ANS04 = 'The multisig escrow holders of Crypto*Trade 2.0.2 is @jslim162, @JamesG07 or @okcoin. You may seek help immediately pertaining to escrow issues'
ANS05 = 'WARNING: Crypto*Trade 2.0 committee will swear to nail you down at all expense, revealing your true identity and social sickness. Report to @jslim162 without delay'
ANS06 = 'WARNING: Crypto*Trade 2.0 community will enjoy peace of mind if you could slowly.. really slow down non-related post or you get booted out. Report to @jslim162 now'
ANS07 = 'Crypto*Trade 2.0.2'
ANS08 = '32EyQiKfmqAz8AA5PcabUVbUsxSxWVif6w \n\n[Bitcoin] Multisig Escrow is now live!! It is available to all and always get ready for a transaction provided maker set the ads post and taker accepted the offer within 10 minutes of timeframe that Escrow Fees: 1% on buyer side. You may PM @jslim162 or @JamesG07 or @okcoin for release of escrow as you will need any 2 of 3 approval. This is the EscrowBot you can trust (Insurance: 0.50 BTC per transaction)'
ANS09 = 'Escrow Fees: 0.3% on buyer side. Eg. Seller deposited 10 BTC in escrow, and you will get 9.97 BTC after completion'
ANS10 = 'EscrowBot is always AML/KYC compliance. Escrow members has duty to enforce it to safeguard open community in niche market. Any violation to our terms and conditions may result your escrow service being rejected. The establishment of escrow is in good faith and the objective is to provide a safe, easy and comfortable place to trade or an opportunity to meet up in Crypto*Trade 2.0'
ANS11 = 'Committee got to screen through verification of escrow members whether they are fit and proper to carry out duty apart from earning a portion of the fees, in case the escrow went burst, the fund will be used to reimburse victim, covering losses up to 0.50 BTC in a transaction'
ANS12 = 'TO: SELLER, \nEscrow is open and ready to deposit /escrowaddress \n\nAre you done already? /yes1 or /no1'
ANS13 = 'TO: BUYER, \nWAIT!! Got to verify bitcoin if it is locked in escrow at https://www.blocktrail.com/BTC/address/32EyQiKfmqAz8AA5PcabUVbUsxSxWVif6w/transactions \n\nIs the amount and timestamp correct? /yes2 or /notsure \nTips: Better safe than sorry!'
ANS14 = 'TO: BUYER & SELLER, \nOnce bitcoin is held in escrow, proceed to fiat payment \n\nBUYER: Have you settled the payment already? /yes3 or /no3 \n\nSELLER: Have you received the fiat payment? /yes4 or /no4'
ANS15 = 'TO: EscrowBot, \nAlert escrow members for release of bitcoin. To check all details and finalize transaction. ***All third party fiat payment will be rejected and return to original source*** \n\nDon\'t forget to review each other! TQ'
ANS16 = 'Escrow procedure is very straight forward and involved 5 simple steps to completion \n\n#. Step1: Check if matching of deal is valid /howtoadspost \n#. Step2: Seller to deposit bitcoin to escrow address \n#. Step3: Semi-automated @EscrowBot to verify if the transaction locked in escrow \n#. Step4: Buyer to make fiat settlement with seller privately \n#. Step5: Escrow members check all details and to release bitcoin to buyer'
ANS17 = 'You may post ads as an offer and the other party has to accept it within 10 minutes to ensure a deal becomes valid. \n\nLearn how to /offeradeal and /acceptadeal'
ANS18 = 'How do you make an offer? \n\nHere is an example: \nWTS> 2 BTC @ MYR5000 each \n\nAnother example:\nWTB> 20.5 BTC for SGD30000 lumpsum'
ANS19 = 'How do you accept an offer? \n\nAlright, let me show you an example: /howtodeal\n\n 1. Reply the message \n 2. DEAL> (letter sensitive and follow bot instructions)\n\nDeal it at your OWN RISK or otherwise get all transactions protected by ESCX Membership or @EscrowBot in case you have a dispute or claims later'
ANS20 = 'Private message @EscrowBot, escrow members for confirmations'
ANS21 = 'Seek help from escrow members, @EscrowBot'
ANS22 = 'Tips1: To accept a deal, always look for \033;/escrownow if available'
ANS23 = 'Tips2: type: help me @EscrowBot'
ANS24 = 'Tips3: Be careful when you dealing with a stranger out there! Crypto*Trade 2.0 is a public group. Scumbags can impersonate you! Man-in-the-middle-attacks are notorous!'
ANS25 = 'Tips4: Some of the escrow features, to issue plugin without dash followed by <botname> \n\n escrow-address \n escrow-members \n escrow-insurance \n escrow-investors \n escrow-fees \n escrow-version \n escrow-rules'
ANS26 = 'Well, you got to tell me first'
ANS27 = 'Tips5: You got to set your username before proceed to deal'
ANS28 = 'Tips6: Always exchange contact details using feature available in Telegram, PM between Buyer and Seller before proceed to a deal'
ANS29 = 'REMINDER Tips7: Crypto*Trade 2.0 takes /scammersowhat and /spammersowhat very seriously who reported publicly about violation, suspicious activity or abusive behaviour will lead to further study by committee and put offender to justice if necessary'
ANS30 = 'Tips8: Share the group link wisely at @c2trade'
ANS31 = 'Escrow statistic \n32EyQiKfmqAz8AA5PcabUVbUsxSxWVif6w \n\nBalance: 0.015818 BTC \nLargest transaction: 0.0 BTC \nAccumulative Escrow: 0.0 BTC \n[Updated: 26.04.16]'
ANS32 = 'How does Crypto*Trade 2.0 work? \n\nWhile in doubt, ask seller to deposit BTC to escrow address before buyer makes any fiat settlement with him. Contact escrow members to release BTC. Don\'t forget to leave traces of logs. It\'s that simple!'
ANS33 = 'Let\'s say you want to BUY, just put tag WTB> followed by your rate and request or similarly, you want to SELL, put tag WTS>'
ANS34 = 'How to become a verify member @c2trade? \n\nYou got to have.. \n\n* Level 1: Individual Profile /setprofile \n* Level 2: Additional Supporting Documents /setproof \n* Level 3: Get Approval /askmoderator \n\nIt gonna take approximately 7 working days to process your application. Stay tuned!'
ANS35 = 'Level 1: Individual Profile \n\n~Go to sign up an account at https://onename.com and ensure that the compulsory username you pick up is tally with Telegram ID you set \n~Fill in your details, you got to have at least the following:- \n~~A clear profile picture, group photos is not acceptable \n~~Full name as per identity with optional 2+3 asterisk to retain some of your privacy \n~~Location, just the name of city of your current residence \n~~Bitcoin address, your ESCX wallet address \n~~Description, your international format cell phone contact number \n~~With at least 2/3 verifications activated, Facebook or Twitter or Github \n\nDownload the Indiesquare apps from Playstore/Appstore at https://wallet.indiesquare.me/ \n\nUse only Indiesquare wallet address for both your BTC and ESCX transactions, all trades made @c2trade from now onwards. Update this wallet address at onename.com profile page. Try not to make low level mistake in your Indiesquare wallet, always remember to backup paper key in your settings and keep it safe'
ANS36 = 'Level 2: Additional Supporting Documents \n\nPrimary Verification - [Proof of Identity] \n~Passport or \n~Driver\'s License or \n~National Identity Card \n\nSecondary Verification - [Proof of Residence] \n~Bank Statement or \n~Utility Bill or \n~Tax Return \n\nTertiary Verification - [Proof of Cellular] \n~SMS \n~Voice'
ANS37 = 'Level 3: Get approval \n\n~Notify moderators once you have set and prepared all items already layout to you. Moderator will verify you in PM. Ensure that your proof of residency is issued no older than 3 months, with all images to be strike out \'FOR Crypto*Trade 2.0 ONLY\' visible at least 300dpi resolution or higher. \n\nWe reserved the rights to use external resources eg. awwapp.com or live webcam to randomly spot check the qualitative membership of traders from time to time. However, you must maintain at least 20 ESCX collateral at all time in GML as active.'
ANS38 = 'It is compulsory that you proceed to verification and comply with our house rules in here. Failure to do so will have you removed from Crypto*Trade 2.0 in 24 hours. \n\nLearn how to get /membership'
ANS39 = 'Tips9: Always say no to third party deal and refer to GML for reputable members only. Local dialect are welcome but do keep it short, nice and friendly! Put price action into focus!'
ANS40 = '1AXgQdNmANYQgu4KXYRFTCKS6A26no9bek'


COM01 = 'help me'
COM02 = 'tip'
COM03 = 'DEAL>'
COM04 = 'escrow address'
COM05 = 'escrow members'
COM06 = 'escrow insurance'
COM07 = 'escrow investors'
COM08 = 'escrow fees'
COM09 = 'escrow version'
COM10 = 'escrow rules'
COM11 = 'WARNING:'
#COM12 = 'GML?'
#COM13 = 'VM?'
#COM14 = 'nVM?'
#COM15 = 'PM?'
COM16 = 'to verify?'
COM17 = 'to deal?'
COM18 = 'treasury address'


ORDER01 = '/aboutme'
ORDER02 = '/howtoadspost'
ORDER03 = '/escrowprocedure'
ORDER04 = '/escrowaddress'
ORDER05 = '/escrowinsurance'
ORDER06 = '/escrowmembers'
ORDER07 = '/escrowstatus'
ORDER08 = '/theruleshere'
ORDER09 = '/scammersowhat'
ORDER10 = '/spammersowhat'
ORDER11 = '/yes1'
ORDER12 = '/yes2'
ORDER13 = '/yes3'
ORDER14 = '/offeradeal'
ORDER15 = '/acceptadeal'
ORDER16 = '/yes4'
ORDER17 = '/no4'

ORDER21 = '/no1'
ORDER22 = '/notsure'
ORDER23 = '/no3'
#ORDER24 = '/review'
#ORDER25 = '/report'
ORDER26 = '/escrownow'
ORDER27 = '/selftour'
ORDER28 = '/membership'
ORDER29 = '/setprofile'
ORDER30 = '/setproof'
ORDER31 = '/askmoderator'
ORDER32 = '/getverify'


# ================================

class EnableStatus(ndb.Model):
    # key name: str(chat_id)
    enabled = ndb.BooleanProperty(indexed=False, default=False)


# ================================

def setEnabled(chat_id, yes):
    es = EnableStatus.get_or_insert(str(chat_id))
    es.enabled = yes
    es.put()

def getEnabled(chat_id):
    es = EnableStatus.get_by_id(str(chat_id))
    if es:
        return es.enabled
    return False


# ================================

class MeHandler(webapp2.RequestHandler):
    def get(self):
        urlfetch.set_default_fetch_deadline(60)
        self.response.write(json.dumps(json.load(urllib2.urlopen(BASE_URL + 'getMe'))))


class GetUpdatesHandler(webapp2.RequestHandler):
    def get(self):
        urlfetch.set_default_fetch_deadline(60)
        self.response.write(json.dumps(json.load(urllib2.urlopen(BASE_URL + 'getUpdates'))))


class SetWebhookHandler(webapp2.RequestHandler):
    def get(self):
        urlfetch.set_default_fetch_deadline(60)
        url = self.request.get('url')
        if url:
            self.response.write(json.dumps(json.load(urllib2.urlopen(BASE_URL + 'setWebhook', urllib.urlencode({'url': url})))))


class WebhookHandler(webapp2.RequestHandler):
    def post(self):
        urlfetch.set_default_fetch_deadline(60)
        body = json.loads(self.request.body)
        logging.info('request body:')
        logging.info(body)
        self.response.write(json.dumps(body))

        update_id = body['update_id']
        message = body['message']
        message_id = message.get('message_id')
        date = message.get('date')
        text = message.get('text')
        fr = message.get('from')
        chat = message['chat']
        chat_id = chat['id']
        

        if not text:
            logging.info('no text')
            return

        def reply(msg=None, img=None):
            if msg:
                resp = urllib2.urlopen(BASE_URL + 'sendMessage', urllib.urlencode({
                    'chat_id': str(chat_id),
                    'text': msg.encode('utf-8'),
                    'disable_web_page_preview': 'true',
                    #'reply_to_message_id': str(message_id),
                })).read()
            elif img:
                resp = multipart.post_multipart(BASE_URL + 'sendPhoto', [
                    ('chat_id', str(chat_id)),
                    #('reply_to_message_id', str(message_id)),
                ], [
                    ('photo', 'image.jpg', img),
                ])
            else:
                logging.error('no msg or img specified')
                resp = None

            logging.info('send response:')
            logging.info(resp)

        if text.startswith('/'):
            if text == '/start':
                reply('Bot enabled')
                setEnabled(chat_id, True)
            elif text == ORDER26 or text == ORDER26 + MYBOTNAME:
#                reply(random.choice([ANS12, ANS12]))
                reply('You got to accept DEAL first!')
            elif text == ORDER27 or text == ORDER27 + MYBOTNAME:
                reply(random.choice([ANS16, ANS17, ANS18, ANS19, ANS32, ANS33, ANS34, ANS39, ANS24, ANS25, ANS27, ANS28, ANS29]))
            elif text == ORDER01 or text == ORDER01 + MYBOTNAME:
                reply(random.choice([ANS08, ANS01]))
            elif text == ORDER02 or text == ORDER02 + MYBOTNAME:
                reply(random.choice([ANS17, ANS17]))
            elif text == ORDER03 or text == ORDER03 + MYBOTNAME:
                reply(random.choice([ANS16, ANS16]))
            elif text == ORDER04 or text == ORDER04 + MYBOTNAME:
                reply(random.choice([ANS02, ANS02]))
            elif text == ORDER05 or text == ORDER05 + MYBOTNAME:
                reply(random.choice([ANS03, ANS03]))
            elif text == ORDER06 or text == ORDER06 + MYBOTNAME:
                reply(random.choice([ANS04, ANS04]))
            elif text == ORDER07 or text == ORDER07 + MYBOTNAME:
                reply(random.choice([ANS31, ANS31]))
            elif text == ORDER08 or text == ORDER08 + MYBOTNAME:
                reply(random.choice([ANS29, ANS29]))
            elif text == ORDER09 or text == ORDER09 + MYBOTNAME:
                reply(random.choice([ANS05, ANS05]))
            elif text == ORDER10 or text == ORDER10 + MYBOTNAME:
                reply(random.choice([ANS06, ANS06]))
            elif text == ORDER11 or text == ORDER11 + MYBOTNAME:
                reply(random.choice([ANS13, ANS13]))
            elif text == ORDER12 or text == ORDER12 + MYBOTNAME:
                reply(random.choice([ANS14, ANS14]))
            elif text == ORDER13 or text == ORDER13 + MYBOTNAME:
                reply(ANS15)
            elif text == ORDER14 or text == ORDER14 + MYBOTNAME:
                reply(random.choice([ANS18, ANS18]))
            elif text == ORDER15 or text == ORDER15 + MYBOTNAME:
                reply(random.choice([ANS19, ANS19]))
            elif text == ORDER16 or text == ORDER16 + MYBOTNAME:
                reply(ANS15)
            elif text == ORDER17 or text == ORDER17 + MYBOTNAME:
                reply(ANS21)
            elif text == ORDER21 or text == ORDER21 + MYBOTNAME:
                reply(random.choice([ANS21, ANS21]))
            elif text == ORDER22 or text == ORDER22 + MYBOTNAME:
                reply(random.choice([ANS20, ANS20]))
            elif text == ORDER23 or text == ORDER23 + MYBOTNAME:
                reply(ANS21)
            elif text == ORDER28 or text == ORDER28 + MYBOTNAME:
                reply(random.choice([ANS34, ANS34]))
            elif text == ORDER29 or text == ORDER29 + MYBOTNAME:
                reply(random.choice([ANS35, ANS35]))
            elif text == ORDER30 or text == ORDER30 + MYBOTNAME:
                reply(random.choice([ANS36, ANS36]))
            elif text == ORDER31 or text == ORDER31 + MYBOTNAME:
                reply(random.choice([ANS37, ANS37]))
            elif text == ORDER32 or text == ORDER32 + MYBOTNAME:
                reply(random.choice([ANS34, ANS34]))
            elif text == '/stop':
                reply('Bot disabled')
                setEnabled(chat_id, False)
            elif text == '/howtodeal':
                file = cStringIO.StringIO(urllib.urlopen('https://image.ibb.co/hrwjdk/howtodeal.jpg').read())
                img = Image.open(file)
                reply(img=file.getvalue())
                #img = Image.new('RGB', (512, 512))
                #base = random.randint(0, 16777216)
                #pixels = [base+i*j for i in range(512) for j in range(512)]  # generate sample image
                #img.putdata(pixels)
                #output = StringIO.StringIO()
                #img.save(output, 'JPEG')
                #reply(img=output.getvalue())
            #else:
                #reply('How can I help you?')

        # CUSTOMIZE FROM HERE

        elif COM01 in text:
            reply(random.choice([ANS16, ANS17, ANS18, ANS19]))
        elif COM02 in text:
            reply(random.choice([ANS22, ANS23, ANS24, ANS25, ANS26, ANS27, ANS28, ANS29, ANS30]))
        elif COM03 in text:
            reply(random.choice([ANS12, ANS12]))
        elif COM04 in text:
            reply(random.choice([ANS02, ANS02]))
        elif COM05 in text:
            reply(random.choice([ANS04, ANS04]))
        elif COM06 in text:
            reply(random.choice([ANS03, ANS03]))
        elif COM07 in text:
            reply(random.choice([ANS11, ANS11]))
        elif COM08 in text:
            reply(random.choice([ANS09, ANS09]))
        elif COM09 in text:
            reply(random.choice([ANS07, ANS07]))
        elif COM10 in text:
            reply(random.choice([ANS10, ANS10]))
        elif COM11 in text:
            reply(ANS38)
        elif COM16 in text:
            reply(ANS34)
        elif COM17 in text:
            reply(ANS19)
        elif COM18 in text:
            reply(ANS40)
        else:
            if getEnabled(chat_id):
                try:
                    resp1 = json.load(urllib2.urlopen('http://www.simsimi.com/requestChat?lc=en&ft=1.0&req=' + urllib.quote_plus(text.encode('utf-8'))))
                    back = resp1.get('res').get('msg')
                except urllib2.HTTPError, err:
                    logging.error(err)
                    back = str(err)
                if not back:
                    reply('okay...')
                elif 'I HAVE NO RESPONSE' in back:
                    reply('Say something to me, can you hear me?')
                else:
                    reply(back)
            else:
                logging.info('not enabled for chat_id {}'.format(chat_id))


app = webapp2.WSGIApplication([
    ('/me', MeHandler),
    ('/updates', GetUpdatesHandler),
    ('/set_webhook', SetWebhookHandler),
    ('/webhook', WebhookHandler),
], debug=True)
