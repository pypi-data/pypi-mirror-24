define(['jquery', 'assetman', 'pytsite-lang', 'pytsite-http-api'], function ($, assetman, lang, httpApi) {
    return function (widget) {
        window.CKEDITOR_BASEPATH = '/assets/pytsite.ckeditor/ckeditor/';

        assetman.loadCSS('pytsite.ckeditor@ckeditor/skins/moono/editor.css');
        assetman.loadJS('pytsite.ckeditor@ckeditor/ckeditor.min.js');
        assetman.loadJS('pytsite.ckeditor@ckeditor/adapters/jquery.js');

        widget.em.find('textarea').each(function () {
            var editor = $(this).ckeditor({
                title: false,
                extraPlugins: 'youtube,codesnippet,stylescombo',
                language: lang.current(),
                filebrowserUploadUrl: httpApi.url('file'),
                height: 500,
                toolbar: [
                    ['Bold', 'Italic', '-', 'Underline', 'Strike', '-', 'Subscript', 'Superscript', '-', 'Format', 'RemoveFormat'],
                    ['NumberedList', 'BulletedList', '-', 'Outdent', 'Indent', '-', 'Blockquote', '-', 'JustifyLeft', 'JustifyCenter', 'JustifyRight'],
                    ['Link', 'Unlink'],
                    ['PasteText', 'PasteFromWord', '-', 'Undo', 'Redo'],
                    ['Image', 'Youtube', 'CodeSnippet', 'Iframe', 'Table', 'HorizontalRule', 'SpecialChar', 'Styles'],
                    ['ShowBlocks', 'Source', 'Maximize']
                ],
                coreStyles_italic: {
                    element: 'i'
                },
                extraAllowedContent: 'div p blockquote img ul ol li a i;span[data-*,hidden,lang](*);script[*];code(*);pre(*)',
                disableNativeSpellChecker: false
            }).editor;

            editor.on('change', function () {
                this.updateElement();
            });
        });
    }
});
