from django.conf.urls import patterns

urlpatterns = patterns(
    'main.views',

    # Legends views
    (r'^$',
        'index.index'),
    (r'^view_deadline/$',
        'index.view_deadline'),
#    (r'^(?P<round_id>\d+)/view_run_home/$',
#        'view_run_home'),

    # Tips views
    (r'^(?P<round_id>\d+)/tips/$',
        'tips_and_results.view_tips'),

    # Results views
    (r'^(?P<round_id>\d+)/submit_results/$',
        'tips_and_results.get_results'),

    # Ladder views
    (r'^(?P<round_id>\d+)/ladders/$',
        'ladders.view_ladder'),
    (r'^(?P<round_id>\d+)/(?P<view_name>view_\w+_ladder)/$',
        'ladders.view_ladder'),

    # Stats views
    (r'^stats/$',
        'stats.view_stats'),
    (r'^stats/score_detail_form/$',
        'stats.render_ladder_selector'),
    (r'^stats/score_detail/(?P<fixture_id>\d+)/$',
        'stats.score_detail'),
    (r'^stats/bye_score_detail/(?P<bye_id>\d+)/$',
        'stats.bye_score_detail'),
    (r'^stats/score_detail_header/(?P<fixture_id>\d+)/$',
        'stats.score_detail_header'),
    (r'^stats/bye_score_detail_header/(?P<bye_id>\d+)/$',
        'stats.bye_score_detail_header'),
    (r'^stats/(?P<view_name>\w+)/$',
        'stats.view_stats'),
    (r'^stats/(?P<view_name>\w+)/(?P<season_id>\d+)/$',
        'stats.view_stats'),
    (r'^stats/(?P<view_name>coach_v_coach)/(?P<coach_1>[\w ]+)/(?P<coach_2>[\w ]+)/$',
        'stats.view_stats'),
    (r'^stats/(?P<view_name>\w+)/(?P<season_id>\d+)/(?P<round_id>\d+)/$',
        'stats.view_stats'),
    (r'^stats/(?P<view_name>\w+)/(?P<season_id>\d+)/(?P<round_id>\d+)/(?P<ladder>\w+)/$',
        'stats.view_stats'),
    (r'^stats/(?P<view_name>\w+)/(?P<season_id>\d+)/(?P<round_id>\d+)/(?P<ladder>\w+)/(?P<sort_key>\w+)/$',
        'stats.view_stats'),
    (r'^stats/(?P<view_name>\w+)/(?P<season_id>\d+)/(?P<ladder>\w+)/$',
        'stats.view_stats'),

    # Admin views
    (r'^admin/$',
        'admin.view_admin'),
    (r'^admin/(?P<view_name>\w+)/$',
        'admin.view_admin'),
    (r'^admin/(?P<view_name>\w+)/(?P<coach_id>\d+)/$',
        'admin.view_admin'),
)
