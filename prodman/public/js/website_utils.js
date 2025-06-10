// Copyright (c) 2015, nts Technologies Pvt. Ltd. and Contributors
// License: GNU General Public License v3. See license.txt

if (!window.prodman) window.prodman = {};

prodman.subscribe_to_newsletter = function (opts, btn) {
	return nts.call({
		type: "POST",
		method: "nts.email.doctype.newsletter.newsletter.subscribe",
		btn: btn,
		args: { email: opts.email },
		callback: opts.callback,
	});
};
