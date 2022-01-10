import os
import pickle
import matplotlib.pyplot as plt
import streamlit as st
import streamlit.components.v1 as components


# 類似PJを表示する画面
def render_sim_episode():
    st.title("白金鉱業.FM 類似エピソード検索")
    st.caption('エピソードを選択すると、その回と内容が似ているエピソードを表示します。')

    with open('./data/episode_master.pickle', 'rb') as f:
        episode_master = pickle.load(f)
    title_list = [info['title'] for info in [infos for infos in episode_master.values()]]
    title_list.insert(0, '-') # 無選択を意味する'-'を先頭に追加
    selected_episode = st.selectbox('エピソードを選択してください', title_list)
    # 無選択状態の場合は処理を終了
    if selected_episode == '-':
        st.stop()

    # 主体エピソードの情報を表示
    st.markdown('## 対象エピソード')
    target_id = [id for id, info in episode_master.items() if info['title'] == selected_episode][0]
    episode_info = episode_master[target_id]
    st.write('タイトル: {}'.format(episode_info['title']))
    st.write('概要: {}'.format(episode_info['description']))
    st.write('{}'.format(episode_info['url']))

    #主体エピソードのwordcloudの表示
    st.write('wordcloud:')
    fig_dir = './wordcloud_figs'
    fig_names = os.listdir(fig_dir)
    wordcloud_fig = [fig for fig in fig_names if fig == f'{target_id}.png'][0]
    file_name = os.path.join(fig_dir, wordcloud_fig)
    st.image(plt.imread(file_name))

    # 類似PJの表示を表示
    st.markdown('## 類似エピソードtop5')
    with open('./output/cossim_result.pickle', 'rb') as p:
        results = pickle.load(p)

    for idx, result in enumerate(results[target_id][:5]):
        st.write('【類似度{}位】'.format(idx+1), '（コサイン類似度: {:.4f}）'.format(result['cos_sim']))
        st.write('タイトル: {}'.format(result['title']))
        st.write('概要: {}'.format(episode_master[result['episode_id']]['description']))
        st.write(result['url'])

        # wordcloudの表示
        wordcloud_fig = [fig for fig in fig_names if fig == '{}.png'.format(result['episode_id'])][0]
        file_name = os.path.join(fig_dir, wordcloud_fig)
        st.image(plt.imread(file_name), width=400)


# ネットワーク図を表示する画面
def render_episode_network():
    st.title('エピソードネットワーク')
    st.caption('エピソード同士の類似度が0.25以上のペアを抽出し、グラフ化しています。0.25は独断と偏見により「確かに似ている」と感じられる定性的な閾値です。')
    # networkxとpyvisで作成したインタラクティブなネットワーク図のhtmlファイルを読み込んで表示
    # https://towardsdatascience.com/how-to-deploy-interactive-pyvis-network-graphs-on-streamlit-6c401d4c99db
    HtmlFile = open(f'./episode-network_025.html', 'r', encoding='utf-8')
    components.html(HtmlFile.read(), height=600, width=800)


# サイドバー（2画面）形式で表示
def main():
    apps = {
        '類似エピソード検索': render_sim_episode,
        'エピソードネットワーク': render_episode_network
    }
    selected_app_name = st.sidebar.selectbox(label='contents',
                                            options=list(apps.keys()))

    # 選択されたアプリケーションを処理する関数を呼び出す
    render_func = apps[selected_app_name]
    render_func()

if __name__ == '__main__':
    main()
