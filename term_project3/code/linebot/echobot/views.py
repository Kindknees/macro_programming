from django.shortcuts import render
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings

from linebot import LineBotApi, WebhookParser
from linebot.exceptions import InvalidSignatureError, LineBotApiError
from linebot.models import MessageEvent, TextSendMessage, StickerMessage, ImageSendMessage, LocationSendMessage

import xml.etree.ElementTree as et

line_bot_api = LineBotApi(settings.LINE_CHANNEL_ACCESS_TOKEN)
parser = WebhookParser(settings.LINE_CHANNEL_SECRET)


def get_vdlive_speed(time, id):
    namespace = {
        "ns": "http://traffic.transportdata.tw/standard/traffic/schema/"}
    vdlive_tree = et.parse(
        f'../vd_uncompressed_data/{time}.xml')
    vd_lives = vdlive_tree.findall(
        "./ns:VDLives/ns:VDLive", namespace)
    for vd_live in vd_lives:
        link_id = vd_live.find(
            './ns:LinkFlows/ns:LinkFlow/ns:LinkID', namespaces=namespace).text
        if link_id == id:
            sum = 0
            temp = []
            lanes = vd_live.findall(
                "./ns:LinkFlows/ns:LinkFlow/ns:Lanes/ns:Lane", namespace)
            for lane in lanes:
                speed_by_lane = int(
                    lane.find("ns:Speed", namespaces=namespace).text)
                if speed_by_lane != 0:
                    temp.append(speed_by_lane)  # speed_matrix[車道]
            for a in temp:
                sum = sum + a
            avg = sum / len(temp)
    if avg:
        return avg
    else:
        return False


def get_live_traffic_speed(time, id):
    namespace = {
        "ns": "http://traffic.transportdata.tw/standard/traffic/schema/"}
    trafficlive_tree = et.parse(
        f'../livetraffic_uncompressed_data/{time}.xml')
    live_traffics = trafficlive_tree.findall(
        "./ns:LiveTraffics/ns:LiveTraffic", namespaces=namespace)
    for live_traffic in live_traffics:
        section_id = live_traffic.find(
            "./ns:SectionID",  namespaces=namespace).text
        if section_id == id:
            travel_speed = int(live_traffic.find(
                "ns:TravelSpeed",  namespaces=namespace).text)
    if travel_speed:
        return (travel_speed)
    else:
        return False


history = []  # 0:種類 1:時間 2:ID


@csrf_exempt
def callback(request):

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
                if event.message.text == '@VD_data':
                    history.clear()
                    line_bot_api.reply_message(  # 回復傳入的訊息文字
                        event.reply_token,
                        TextSendMessage(text='請輸入你想查到的時間點，時間為1700-2059')
                    )
                    history.append('VD')
                elif event.message.text == '@Live_Traffic_data':
                    history.clear()
                    line_bot_api.reply_message(  # 回復傳入的訊息文字
                        event.reply_token,
                        TextSendMessage(text='請輸入你想查到的時間點，時間為1700-2059')
                    )
                    history.append('Live')
                elif (len(history) == 1):
                    if history[0] == 'VD':
                        history.append(event.message.text)
                        line_bot_api.reply_message(
                            event.reply_token,
                            TextSendMessage(text='請輸入LinkID')
                        )
                    else:
                        history.append(event.message.text)
                        line_bot_api.reply_message(
                            event.reply_token,
                            TextSendMessage(text='請輸入SectionID')
                        )
                elif len(history) == 2:
                    history.append(event.message.text)
                    if history[0] == 'VD':
                        speed = get_vdlive_speed(history[1], history[2])
                        if speed == False:
                            line_bot_api.reply_message(
                                event.reply_token,
                                TextSendMessage(text='格式輸入錯誤或找無資料，請重新輸入!'))
                        else:
                            line_bot_api.reply_message(
                                event.reply_token,
                                TextSendMessage(
                                    text=f'VD速度資料:\n時間:{history[1]}\nLinkID:{history[2]}\n速度:{speed}')
                            )
                    else:
                        speed = get_live_traffic_speed(history[1], history[2])
                        if speed == False:
                            line_bot_api.reply_message(
                                event.reply_token,
                                TextSendMessage(text='格式輸入錯誤或找無資料，請重新輸入!'))
                        else:
                            line_bot_api.reply_message(
                                event.reply_token,
                                TextSendMessage(
                                    text=f'Live Traffic速度資料:\n時間:{history[1]}\nLinkID:{history[2]}\n速度:{speed}')
                            )
                    history.clear()
                else:
                    line_bot_api.reply_message(
                        event.reply_token,
                        TextSendMessage(text='你在公殺毀?我聽瞴啦'))
        return HttpResponse()
    else:
        return HttpResponseBadRequest()
