return new Promise(function(resolve, reject) {
    grecaptcha.ready(function() {
        grecaptcha.execute('{{RECAPTCHA_SITE_KEY}}', { action: 'adminLogin' })
            .then(function(token) {
                resolve(token);
            })
            .catch(function(error) {
                reject(error);
            });
    });
});
