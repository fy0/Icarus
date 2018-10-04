module.exports = {
    root: true,
    env: {
        node: true
    },
    'extends': [
        'plugin:vue/essential',
        '@vue/standard'
    ],
    rules: {
        'no-console': process.env.NODE_ENV === 'production' ? 'error' : 'off',
        'no-debugger': process.env.NODE_ENV === 'production' ? 'error' : 'off',
        // indent 4 spaces
        'indent': ['error', 4, { 'SwitchCase': 1 }],
        // allow paren-less arrow functions
        'arrow-parens': 0,
        // allow async-await
        'generator-star-spacing': 0
    },
    parserOptions: {
        parser: 'babel-eslint'
    },
    'globals': {
        '$': true,
        '_': true
    }
}
