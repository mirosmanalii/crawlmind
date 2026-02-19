export interface ObservationPayload {
  dom: string;
  signals: {
    statusCode?: number;
    console: {
      errors: string[];
      warnings: string[];
    };
    network: {
      failedRequests: number;
      requestErrors: string[];
    };
    performance: {
      loadTimeMs?: number;
    };
    redirects: string[];
  };
}
