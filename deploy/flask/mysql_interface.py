import database

if __name__ == '__main__':
    db = database.DBHandler()

    # 插入商品 amount 到 json
    #db.set_db_market_info_amount("547083804150464513", "BTC/USDT", 10)

    # 更新 lv2_cert with "Yes" or "No"
    #db.set_lv2_cert("547083804150464513", "Yes")