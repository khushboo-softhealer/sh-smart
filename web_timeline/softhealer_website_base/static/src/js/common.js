odoo.define("softhealer_website_base.common_js", function (require) {
    "use strict";

    var publicWidget = require("web.public.widget");

    publicWidget.registry.BaseCommonJs = publicWidget.Widget.extend({
        selector: "#wrapwrap",
        start: function () {
            // Tooltip init
            $('[data-bs-toggle="tooltip"]').tooltip();

            // Country/State filtering logic
            const form_class = document.querySelector('.sh_custom_website_form_address_fields');
            if (form_class) {
                const countrySelect = document.querySelector('select[name="sh_country_id"]');
                const stateSelect = document.querySelector('select[name="sh_state_id"]');
                const allStateOptions = Array.from(stateSelect.options);

                function filterStates() {
                    const countryID = countrySelect.value;
                    stateSelect.innerHTML = ''; // Clear all options first

                    // Always add the placeholder option
                    const placeholderOption = document.createElement("option");
                    placeholderOption.text = "State";
                    placeholderOption.disabled = true;
                    placeholderOption.selected = true;
                    placeholderOption.value = "";
                    stateSelect.appendChild(placeholderOption);

                    let hasMatchingStates = false;

                    // Append matching state options if a country is selected
                    if (countryID) {
                        allStateOptions.forEach(opt => {
                            if (opt.dataset.country_id === countryID) {
                                const clonedOpt = opt.cloneNode(true);
                                stateSelect.appendChild(clonedOpt);
                                hasMatchingStates = true;
                            }
                        });
                    }

                    // Make the state field required only if there are matching states
                    if (hasMatchingStates) {
                        stateSelect.removeAttribute("disabled");
                        stateSelect.setAttribute("required", "required");
                    } else {
                        stateSelect.removeAttribute("required");
                        stateSelect.setAttribute("disabled", "disabled");
                    }
                }

                if (countrySelect) {
                    countrySelect.addEventListener('change', filterStates);
                    // filterStates(); // Run once on load
                }
            }

            return this._super.apply(this, arguments);
        },
    });
});
