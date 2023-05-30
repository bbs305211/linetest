from django.conf import settings

from linebot import LineBotApi
from linebot.models import TextSendMessage,ImageSendMessage ,TemplateSendMessage,ImageCarouselColumn , ImageCarouselTemplate, MessageTemplateAction
import http.client, json
import re
from test1api.models import users

line_bot_api = LineBotApi(settings.LINE_CHANNEL_ACCESS_TOKEN)

host = 'test20200415.azurewebsites.net'
endpoint_key = "74afa632-9ca7-4281-945d-8871002b024e"  
kb = "97a738b2-cb46-47bc-9e4f-b883fb6058b6" 
method = "/qnamaker/knowledgebases/" + kb + "/generateAnswer"

def sendUse(event):  #使用說明
    try:
        text1 ='''
這是亞洲水泥的智能客服機器人，
請輸入關於亞洲水泥相關問題。
               '''
        message = TextSendMessage(
            text = text1
        )
        line_bot_api.reply_message(event.reply_token,message)
    except:
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text='發生錯誤！'))

def sendQnA(event, mtext):  #QnA
    question = {
        'question': mtext,
    }
    content = json.dumps(question)
    headers = {
        'Authorization': 'EndpointKey ' + endpoint_key,
        'Content-Type': 'application/json',
        'Content-Length': len(content)
    }
    conn = http.client.HTTPSConnection(host)
    conn.request ("POST", method, content, headers)
    response = conn.getresponse ()
    result = json.loads(response.read())
    result1 = result['answers'][0]['answer']
    if 'No good match found in KB.' in result1:
       # msg = '很抱歉，資料庫中無適當解答！\n請再輸入問題。'
        userid = event.source.user_id
        unit = users.objects.create(uid=userid, question=mtext)
        unit.save()
        message = TextSendMessage(
           text = '很抱歉，資料庫中無適當解答！\n請再輸入問題。'
      )
    else:
      pattern = re.compile('(https://[a-zA-Z0-9$-_@.&+\)]+g)') 
      list1=re.findall(pattern,result1)
    

    
    if len(list1)!=0:
          text2= re.sub('\n\n(\!\[\d{1}\]\(https://[a-zA-Z0-9$-_@.&+]+)',"",result1)
          pic=re.findall(pattern,result1)
          '''
          print(list1)
          print(pic)
          '''
          message=[]
          message.append( TextSendMessage(
           text = text2
                           ))
          for i in range(len(list1)):
               message.append(ImageSendMessage(  #傳送圖片
               original_content_url = pic[i],
               preview_image_url = pic[i]
               ))
               '''
               message =[ImageSendMessage(  #傳送圖片
                   original_content_url = pic[i-1],
                   preview_image_url = pic[i-1]
                   ),
                   ImageSendMessage(  #傳送圖片
                   original_content_url = pic[i],
                   preview_image_url = pic[i]
                   )]
                
               '''
         
            
           
    else : message = TextSendMessage(
           text = result1
      )
              
    line_bot_api.reply_message(event.reply_token,message)
