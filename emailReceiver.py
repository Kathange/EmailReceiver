import imaplib
import email
from email.header import decode_header
from email.utils import parsedate_to_datetime
from datetime import datetime, timedelta
import pytz  # 需要安裝 pytz 模塊來處理時區
# from win10toast import ToastNotifier

# 設置 IMAP 伺服器和帳戶信息
IMAP_SERVER = 'imap.gmail.com'
EMAIL_ACCOUNT_1 = 'your_email1@gmail.com'
EMAIL_PASSWORD_1 = 'your_email_password'
EMAIL_ACCOUNT_2 = 'your_email2@gmail.com'
EMAIL_PASSWORD_2 = 'your_email_password'

def get_emails(EMAIL_ACCOUNT, EMAIL_PASSWORD):
    try:
        # 連接到 IMAP 伺服器
        mail = imaplib.IMAP4_SSL(IMAP_SERVER)
        mail.login(EMAIL_ACCOUNT, EMAIL_PASSWORD)

        # 選擇收件箱
        mail.select('inbox')

        # 計算1天前的時間
        ago = (datetime.now() - timedelta(days=7))
        date_since = ago.strftime('%d-%b-%Y')

        # 搜索1天內的所有郵件
        result, data = mail.search(None, '(SINCE "{}")'.format(date_since))
        mail_ids = data[0].split()

        # 獲取當前本地時區
        local_tz = pytz.timezone('Asia/Taipei')  # 替換為你的時區，如 'Asia/Taipei'

        # toaster = ToastNotifier()
        notification_content = ""
        print(f'EMAIL_ACCOUNT : {EMAIL_ACCOUNT}\n')
        notification_content += f'EMAIL_ACCOUNT : {EMAIL_ACCOUNT}\n\n'

        for mail_id in mail_ids:
            result, msg_data = mail.fetch(mail_id, '(RFC822)')
            for response_part in msg_data:
                if isinstance(response_part, tuple):
                    msg = email.message_from_bytes(response_part[1])
                    subject, encoding = decode_header(msg['Subject'])[0]
                    if isinstance(subject, bytes):
                        subject = subject.decode(encoding or 'utf-8')

                    from_ = msg.get('From')
                    date_ = msg.get('Date')
                    
                    # 解析日期並轉換為本地時間
                    parsed_date = parsedate_to_datetime(date_)
                    utc_date = parsed_date.replace(tzinfo=pytz.utc)
                    local_date = utc_date.astimezone(local_tz)
                    formatted_date = local_date.strftime('%Y/%m/%d (%a) %H:%M:%S')

                    print(f'日期: {formatted_date}')
                    print(f'主題: {subject}\n')
                    notification_content += f'日期: {formatted_date}\n'
                    notification_content += f'主題: {subject}\n\n'
        
        # # 使用 Windows 通知
        # if notification_content:
        #     notification_content += '\n\n'
        #     toaster.show_toast("郵件通知", notification_content, duration=10)

        # # 計算日期範圍
        # start_date = ago.strftime('%Y%m%d')
        # end_date = datetime.now().strftime('%Y%m%d')

        # # 將郵件內容寫入到 .txt 文件中
        # with open(f"{EMAIL_ACCOUNT}_{start_date}-{end_date}.txt", "w", encoding="utf-8") as file:
        #     file.write(notification_content)

        mail.logout()

    except Exception as e:
        print(f'檢索郵件失敗: {e}')
        notification_content += f'檢索郵件失敗: {e}\n'


# 手動運行以檢索過去1天內的郵件
if __name__ == "__main__":
    get_emails(EMAIL_ACCOUNT_1, EMAIL_PASSWORD_1)
    get_emails(EMAIL_ACCOUNT_2, EMAIL_PASSWORD_2)
    input("\n\n\n\n程式執行結束，請按任意鍵退出")
