class MessageBox {
    constructor(options) {
        // 把传递进来的配置信息挂载到实例上（以后可以基于实例在各个方法各个地方拿到这个信息）
        for (let key in options) {
            if (!options.hasOwnProperty(key)) break;
            this[key] = options[key];
        }

        // 开始执行
        this.init();
    }
    // 初始化：通过执行INIT控制逻辑的进行
    init() {
        if (this.status === "message") {
            this.createMessage();
            this.open();
            return;
        }

    }
    // 创建元素
    createMessage() {
        this.messageBox = document.createElement('div');
        this.messageBox.className = `dpn-message dpn-${this.type}`;
        this.messageBox.innerHTML = `
        ${this.message}
        <i class="dpn-close">×</i>
    `;
        document.body.appendChild(this.messageBox);

        // 基于事件委托监听关闭按钮的点击
        this.messageBox.onclick = ev => {
            let target = ev.target;
            //判断点击的元素是否为关闭按钮
            if (target.className === "dpn-close") {
                // 点击的是关闭按钮
                this.close();
            }
        };

        // 钩子函数
        this.oninit();
    }

    // 控制显示
    open() {
        if (this.status === "message") {
            let messageBoxs = document.querySelectorAll('.dpn-message'),
                len = messageBoxs.length;
            //计算新弹出的messageBox的Y轴偏移量
            this.messageBox.style.top = `${len === 1 ? 20 : 20 + (len - 1) * 70}px`;

            // 如果duration不为零，控制自动消失
            this.autoTimer = setTimeout(() => {
                this.close();
            }, this.duration);

            // 钩子函数
            this.onopen();
            return;
        }
    }
    // 控制隐藏
    close() {
        if (this.status === "message") {
            clearTimeout(this.autoTimer);
            this.messageBox.style.top = '-200px';
            let anonymous = () => {
                document.body.removeChild(this.messageBox);
                // 钩子函数
                this.onclose();
            };
            this.messageBox.addEventListener('transitionend', anonymous);
            return;
        }

    }
}

//全局对象上挂载该方法
window.messageplugin = function (options = {}) {
    //允许只传入字符串，对其进行对象格式处理
    if (typeof options === "string") {
        options = {
            message: options
        };
    }
    //用户提供的配置覆盖默认配置项
    options = Object.assign({
        status: 'message',
        message: '我是默认信息',
        type: 'info',
        duration: 1500,
        //生命周期钩子
        oninit() { },
        onopen() { },
        onclose() { },
    }, options);
    return new MessageBox(options);
};

// 游戏进程找不到的通知
window.game_not_start = () => {
    messageplugin({
        message: "请先开启游戏进程，并点击右上角刷新按钮！",
        type: "warning"
    })
}

window.addEventListener('mousewheel', function (event) {
    if (event.ctrlKey === true || event.metaKey) {
        event.preventDefault();
    }
}, { passive: false });

//firefox
window.addEventListener('DOMMouseScroll', function (event) {
    if (event.ctrlKey === true || event.metaKey) {
        event.preventDefault();
    }
}, { passive: false });
//+_
window.onload = function () {
    document.addEventListener('keydown', function (event) {
        if ((event.ctrlKey === true || event.metaKey === true)
            && (event.which === 61 || event.which === 107
                || event.which === 173 || event.which === 109
                || event.which === 187 || event.which === 189)) {
            event.preventDefault();
        }
    }, false);
}