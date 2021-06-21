function parseURL() {
    const search = window.location.search
    const id = search.match(/id=[a-zA-Z0-9]+/)[0].slice(3)
    const link = search.match(/link=%22.+%22/)[0]
    return [id, parseTransactionURL(link.slice(8, link.length - 3))]
}

function getRawURL() {
    const search = window.location.search
    ans = null
    for(var i = 0; i < search.length; ++i){
        if(search[i] == '?'){
            ans = i;
            break;
        }
    }
    if(ans != null) ans = search.substr(0,ans);
    return ans
}

function parseTransactionURL(uri) {
    if (!uri || typeof uri !== 'string') {
        throw new Error('uri must be a string')
    }

    if (uri.substring(0, 9) !== 'ethereum:') {
        throw new Error('Not an Ethereum URI')
    }

    let prefix
    let address_regex = '(0x[\\w]{40})'


    if (uri.substring(9, 11).toLowerCase() === '0x') {
        prefix = null
    } else {
        let cutOff = uri.indexOf('-', 9)

        if (cutOff === -1) {
            throw new Error('Missing prefix')
        }
        prefix = uri.substring(9, cutOff)
        const rest = uri.substring(cutOff + 1)

        // Adapting the regex if ENS name detected
        if (rest.substring(0, 2).toLowerCase() !== '0x') {
            address_regex = '([a-zA-Z0-9][a-zA-Z0-9-]{1,61}[a-zA-Z0-9]\.[a-zA-Z]{2,})'
        }
    }

    const full_regex = '^ethereum:(' + prefix + '-)?' + address_regex + '\\@?([\\w]*)*\\/?([\\w]*)*'

    const exp = new RegExp(full_regex)
    const data = uri.match(exp)
    if (!data) {
        throw new Error('Couldnot not parse the url')
    }

    let parameters = uri.split('?')
    parameters = parameters.length > 1 ? parameters[1] : ''
    const params = Qs.parse(parameters)

    const obj = {
        scheme: 'ethereum',
        target_address: data[2]
    }

    if (prefix) {
        obj.prefix = prefix
    }

    if (data[3]) {
        obj.chain_id = data[3]
    }

    if (data[4]) {
        obj.function_name = data[4]
    }

    if (Object.keys(params).length) {
        obj.parameters = params
        const amountKey = obj.function_name === 'transfer' ? 'uint256' : 'value'

        if (obj.parameters[amountKey]) {
            obj.parameters[amountKey] = new BigNumber(obj.parameters[amountKey], 10).toString()
            if (!isFinite(obj.parameters[amountKey])) throw new Error('Invalid amount')
            if (obj.parameters[amountKey] < 0) throw new Error('Invalid amount')
        }
    }

    return obj
}


async function main() {
    window.web3 = new Web3(web3.currentProvider)

    await ethereum.enable()

    let id, tx
    [id, tx] = parseURL()

    const transactionParameters = {
        gasPrice: '2540be400',
        gas: '5208',
        to: tx.target_address,
        from: ethereum.selectedAddress,
        value: BigNumber(tx.parameters.value, 10).toString(16),
        data: '',
        chainId: tx.chain_id
    }

    const response = await new Promise((res, rej) => ethereum.sendAsync({
        method: 'eth_sendTransaction',
        params: [transactionParameters],
        from: ethereum.selectedAddress,
    }, (err, result) => err ? rej(err) : res(result)))

    rawURL = getRawURL()
    var xhttp = new XMLHttpRequest();
    xhttp.open("POST", rawURL, true);
    xhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    xhttp.send("id="+String(id)+"&from="+String(ethereum.selectedAddress)+"&to="+String(tx.target_address)+"&status=1");


    document.getElementById('id').innerHTML = id
    document.getElementById('hash').innerHTML = response.result
    document.getElementById('link').innerHTML = `<a href='https://kovan.etherscan.io/tx/${response.result}'>link</a>`
    alert("Transfer confirmed")
}
