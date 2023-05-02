export class RunningAverageDeque {
    constructor(starting_array=[]) {
      this.items = starting_array;
      this.sum = this.items.reduce((acc, curr) => acc + curr, 0);
      this.average = this.sum / this.items.length;
    }

    popFrontPushBack(element) {
        item = this.items.shift();
        this.sum -= item
        this.items.push(element);
        this.sum += element;
        this.average = self.getAverage()
        return item;
    }
  
    peekFront() {
      return this.items[0];
    }
  
    peekBack() {
      return this.items[this.items.length - 1];
    }
  
    isEmpty() {
      return this.items.length === 0;
    }
  
    size() {
      return this.items.length;
    }

    getAverage() {
        if (this.isEmpty()) return 0;
        return this.sum / this.size();
    }
  }
  