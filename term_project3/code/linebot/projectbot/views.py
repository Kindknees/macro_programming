from django.shortcuts import render
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings

from linebot import LineBotApi, WebhookParser
from linebot.exceptions import InvalidSignatureError, LineBotApiError
from linebot.models import MessageEvent, TextSendMessage, StickerMessage, ImageSendMessage, LocationSendMessage
# import openai

# openai.api_key = settings.OPENAI_SECRET
line_bot_api = LineBotApi(settings.LINE_CHANNEL_ACCESS_TOKEN)
parser = WebhookParser(settings.LINE_CHANNEL_SECRET)

# chat_button = False
# history = []


""" def chat(message):

    history.append(
        {
            'role': 'user',
            'content': message+'，請用繁體中文回答'
        }
    )

    response = openai.chat.completions.create(
        model='gpt-3.5-turbo',
        messages=history
    )
    response_message = response.choices[0].message

    history.append(
        {
            'role': response_message.role,
            'content': response_message.content
        }
    )

    return response_message.content """


@csrf_exempt
def callback(request):

    global chat_button

    if request.method == 'POST':
        signature = request.META['HTTP_X_LINE_SIGNATURE']
        body = request.body.decode('utf-8')

        try:
            events = parser.parse(body, signature)  # 傳入的事件
        except InvalidSignatureError:
            return HttpResponseForbidden()
        except LineBotApiError:
            return HttpResponseBadRequest()

        for event in events:
            if isinstance(event, MessageEvent):  # 如果有訊息事件
                if event.message.text == 'hello':
                    line_bot_api.reply_message(  # 回復傳入的訊息文字
                        event.reply_token,
                        TextSendMessage(text='hahaha')
                    )
                elif event.message.text == '@sticker':
                    try:
                        message = StickerMessage(
                            package_id='6136',
                            sticker_id='10551377'
                        )
                        line_bot_api.reply_message(event.reply_token, message)
                    except:
                        line_bot_api.reply_message(
                            event.reply_token,
                            TextSendMessage(text='loading....')
                        )
                elif event.message.text == '@photo':
                    try:
                        image_message = ImageSendMessage(
                            original_content_url='https://pbs.twimg.com/profile_images/433716924166709248/B3qaZuaD.jpeg',
                            preview_image_url='https://pbs.twimg.com/profile_images/433716924166709248/B3qaZuaD.jpeg'
                        )
                        line_bot_api.reply_message(
                            event.reply_token, image_message)
                    except:
                        line_bot_api.reply_message(
                            event.reply_token,
                            TextSendMessage(text='loading....')
                        )
                elif event.message.text == '@location':
                    try:
                        location_message = LocationSendMessage(
                            title='國立陽明交通大學 工程三館',
                            address='300新竹市東區大學路1001號工程三館',
                            latitude='24.78714926497548',
                            longitude='120.99796872181692'
                        )
                        line_bot_api.reply_message(
                            event.reply_token, location_message)
                    except:
                        line_bot_api.reply_message(
                            event.reply_token,
                            TextSendMessage(text='loading....')
                        )
                # elif event.message.text == '@chatgpt':
                #     chat_button = not chat_button

                #     if chat_button == True:
                #         history.clear()
                #         line_bot_api.reply_message(
                #             event.reply_token,
                #             TextSendMessage(text='ChatGPT is on:')
                #         )
                #     else:
                #         line_bot_api.reply_message(
                #             event.reply_token,
                #             TextSendMessage(text='ChatGPT is off:')
                #         )
                # elif chat_button:
                #     try:
                #         reply = chat(event.message.text.strip())
                #         line_bot_api.reply_message(
                #             event.reply_token,
                #             TextSendMessage(text=reply)
                #         )
                #     except:
                #         line_bot_api.reply_message(
                #             event.reply_token,
                #             TextSendMessage(
                #                 text='something is wrong with ChatGPT')
                #         )
                elif event.message.text == '@gift':
                    try:
                        line_bot_api.reply_message(
                            event.reply_token,
                            TextSendMessage(text='請輸入年齡')
                        )
                    except:
                        line_bot_api.reply_message(
                            event.reply_token,
                            TextSendMessage(text='loading....')
                        )
                elif event.message.text == '18':
                    try:
                        line_bot_api.reply_message(
                            event.reply_token,
                            TextSendMessage(text='請輸入性別')
                        )
                    except:
                        line_bot_api.reply_message(
                            event.reply_token,
                            TextSendMessage(text='loading....')
                        )
                elif event.message.text == '瑟瑟':
                    try:
                        image_message = ImageSendMessage(
                            original_content_url='https://s.yimg.com/ny/api/res/1.2/hzOSgymr6hIF8daJuJM1pA--/YXBwaWQ9aGlnaGxhbmRlcjtoPTY2Ng--/https://s.yimg.com/os/creatr-uploaded-images/2021-09/4fd0c420-1c3c-11ec-b1ff-ea1868351416',
                            preview_image_url='https://s.yimg.com/ny/api/res/1.2/hzOSgymr6hIF8daJuJM1pA--/YXBwaWQ9aGlnaGxhbmRlcjtoPTY2Ng--/https://s.yimg.com/os/creatr-uploaded-images/2021-09/4fd0c420-1c3c-11ec-b1ff-ea1868351416'
                        )
                        line_bot_api.reply_message(
                            event.reply_token, image_message)
                    except:
                        line_bot_api.reply_message(
                            event.reply_token,
                            TextSendMessage(text='loading....')
                        )
                else:
                    line_bot_api.reply_message(
                        event.reply_token,
                        TextSendMessage(
                            text="以下幫你挑了幾項禮物:\n1.**驚喜型:\n驚喜旅行：預訂一個周末或短期的旅行，選擇一個她未曾去過或一直夢想去的地方。\n2.**設計型:\n精心準備的晚餐:在家或特別的地點準備一頓精心策劃的晚餐，加上燭光和音樂，營造浪漫氛圍。\n3.**豪華型:\n私人音樂會或表演：如果她喜歡音樂或表演藝術，可以為她安排一場私人音樂會或表演。")
                    )

        return HttpResponse()
    else:
        return HttpResponseBadRequest()
