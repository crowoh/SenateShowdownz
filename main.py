import api_handler
import data_processor
import visualization

def main():
    endpoint = 'https://lda.senate.gov/api/v1/contributions/'  # Replace with actual endpoint
    raw_data = api_handler.get_lobbying_data(endpoint)
    if raw_data:
        processed_data = data_processor.process_data(raw_data)
        visualization.visualize_contributions(processed_data)

if __name__ == "__main__":
    main()