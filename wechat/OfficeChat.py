from wcferry import Wcf
import json



if __name__ == "__main__":
    wcf = Wcf()
    print(wcf.is_login())
    print(wcf.get_self_wxid())
    print(wcf.is_receiving_msg())
    print(wcf.enable_receiving_msg())
    print(wcf.is_receiving_msg())
    # print(wcf.get_contacts())
    # wcf.send_text("能收到吗？\n 我在测试用程序发微信", "wxid_k36lcqhfkqs111")

    print(wcf.get_dbs())
    tables = wcf.get_tables("MSG0.db")
    print(json.dumps(tables, indent=4, ensure_ascii=False))
    # print(wcf.query_sql("ChatMsg.db", "select * from ChatMsg")) WHERE strTalker = 'wxid_k36lcqhfkqs111'
    print(wcf.query_sql("MSG0.db", "SELECT * from MSG WHERE strTalker = 'wxid_k36lcqhfkqs111' AND CreateTime > 1741585146"))