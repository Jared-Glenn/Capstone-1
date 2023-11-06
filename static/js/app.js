const $qrEndpoint = $('#qr-endpoint')

async function getCode(e) {
    e.preventDefault();
    const qrEndpoint = $qrEndpoint.value
}