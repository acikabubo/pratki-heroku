from flask_assets import Bundle

bundles = {

    'js': Bundle(
        'js/info.js',
        output='gen/main.js'),

    'css': Bundle(
        'css/base.css',
        'css/index.css',
        'css/info.css',
        'css/package.css',
        'css/android.css',
        output='gen/main.css'),

    'img': Bundle(
        'img/favicon.ico')

}
