function Countdown(end_time, tick_callback){
    this.end_time = end_time;
    this.start_time = moment();

    this.remaining = parseInt((this.end_time - this.start_time) / 1000);
    this.tick_callback = tick_callback;

    this.timer_callback = function(){
        this.tick_callback(this.remaining);
        this.remaining--;
        if (this.remaining < 0){
            this.stop();
        }
    }.bind(this);

    this.stop = function(){
        clearInterval(this.timer_id);
    }.bind(this);

    this.timer_id = setInterval(this.timer_callback, 1000);

    return this;
}