class IntegrationCosts:
    def __init__(self):
        # WhatsApp costs in Malaysia per API call
        self.whatsapp_costs_malaysia = {
            'marketing': 0.086,
            'utility': 0.02,
            'authentication': 0.018,
            'service': 0.022,
        }

        # Twilio + WhatsApp costs
        self.twilio_whatsapp_costs = {
            'utility': {'conversation': 0.02, 'message': 0.005},
            'service_conversation': {'conversation': 0.0022, 'message': 0.005},
        }

    def get_whatsapp_cost_malaysia(self, api_type, calls):
        """
        Compute the cost for WhatsApp API calls in Malaysia.

        :param api_type: Type of API call. Either 'marketing', 'utility', 'authentication', or 'service'.
        :param calls: Number of API calls.
        :return: Total cost.
        """
        if api_type not in self.whatsapp_costs_malaysia:
            raise ValueError("Invalid API type. Choose either 'marketing', 'utility', 'authentication', or 'service'.")

        cost_per_call = self.whatsapp_costs_malaysia[api_type]
        total_cost = cost_per_call * calls

        return total_cost

    def get_twilio_whatsapp_cost(self, conversation_type, conversations, messages):
        """
        Compute the cost for Twilio + WhatsApp conversations and messages.

        :param conversation_type: Type of conversation. Either 'utility' or 'service_conversation'.
        :param conversations: Number of conversations.
        :param messages: Number of messages.
        :return: Total cost.
        """
        if conversation_type not in self.twilio_whatsapp_costs:
            raise ValueError("Invalid conversation type. Choose either 'utility' or 'service_conversation'.")

        cost_per_conversation = self.twilio_whatsapp_costs[conversation_type]['conversation']
        cost_per_message = self.twilio_whatsapp_costs[conversation_type]['message']
        total_cost = (cost_per_conversation * conversations) + (cost_per_message * messages)

        return total_cost

# # Example usage:
# integration_costs = IntegrationCosts()

# # WhatsApp cost in Malaysia
# api_type = 'utility'
# calls = 10
# whatsapp_cost_malaysia = integration_costs.get_whatsapp_cost_malaysia(api_type, calls)
# print(f"Total cost for {calls} WhatsApp {api_type} API calls in Malaysia: ${whatsapp_cost_malaysia:.2f}")

# # Twilio + WhatsApp cost
# conversation_type = 'utility'
# conversations = 5
# messages = 20
# twilio_whatsapp_cost = integration_costs.get_twilio_whatsapp_cost(conversation_type, conversations, messages)
# print(f"Total cost for {conversations} {conversation_type} conversations and {messages} messages with Twilio + WhatsApp: ${twilio_whatsapp_cost:.2f}")
