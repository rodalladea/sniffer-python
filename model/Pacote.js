let Mongo = require('./mongo');

module.exports = class Pacote extends Mongo {

    constructor(data) {
        super(data);
        this._id = data._id;
        this.timestamp = data.timestamp;
        this.srcIP = data.srcIP;
        this.dstIP = data.dstIP;
        this.L7protocol = data.L7protocol;
        this.size = data.size;
        this.ttl = data.ttl;
        this.srcMAC = data.srcMAC;
        this.dstMAC = data.dstMAC;
        this.L4protocol = data.L4protocol;
        this.srcPort = data.srcPort;
        this.dstPort = data.dstPort;
        this.payload = data.payload;
        this.collection = 'pacote';
    }

    static find(query = {}, limit = 0) {
        return super.find(query, {nome: 1}, limit, 'pacote').then(result => {
            return result.map(pacote => new Pacote(pacote));
        });
    }
    
}
