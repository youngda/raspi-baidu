var BaseBot = require('bot-sdk');
var tcp = require('./tcp')
class Bot extends BaseBot{
    constructor (postData) {
        super(postData);

        this.addLaunchHandler(() => {
            return {
                outputSpeech: '车已就位'
            };
        });

        this.addIntentHandler('car', () => {
            let forward = this.getSlot('forward');
            let back = this.getSlot('back');
            let left = this.getSlot('left');
            let right = this.getSlot('right');
            if (!forward && !back && !left && !right) {
                let card = new Bot.Card.TextCard('请控制' + forward + back + left + right);
                // 可以返回异步 Promise
                return Promise.resolve({
                    card: card,
                    outputSpeech: '你要做什么呢'
                });
            }

            if (this.request.isDialogStateCompleted()) {
                if(forward){
                    let card = new Bot.Card.TextCard('正在前进');
                    tcp.drives[0].write('0')
                    return {
                        card: card,
                        outputSpeech: '前进中'
                    };
                }
                else if(back){
                    let card = new Bot.Card.TextCard('正在前进');
                    tcp.drives[0].write('1')
                    return {
                        card: card,
                        outputSpeech: '后退中'
                    };
                }
                else if(left){
                    let card = new Bot.Card.TextCard('正在前进');
                    tcp.drives[0].write('2')
                    return {
                        card: card,
                        outputSpeech: '左转中'
                    };
                }
                else if(right){
                    let card = new Bot.Card.TextCard('正在前进');
                    tcp.drives[0].write('3')
                    return {
                        card: card,
                        outputSpeech: '右转中'
                    };
                }
            }
        });
    }
}

module.exports = Bot;