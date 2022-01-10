[白金鉱業.FM](https://shirokane-kougyou.fm/)番組内の類似エピソードを検索できます。  
https://share.streamlit.io/ysdyt/shirokanefm_search/main/shirokanefm_similarity.py

ざっくりと、やり方は以下です。
1. Amazon Transcribeでmp3音源を文字起こし
2. 文字起こししたテキスト中の名詞や固有名詞を抽出
3. 抽出した語からエピソード間の類似度を計算
4. 類似度が高い順に表示 （=類似エピソード検索機能）
5. 一定の類似度以上のエピソードペアを抽出してネットワークとして可視化（=エピソードネットワーク）
6. 計算結果データを[streamlit](https://streamlit.io/cloud)でGUIを付けて、[streamlit Cloud](https://streamlit.io/cloud)でホスティングしています。
