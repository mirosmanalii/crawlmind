export interface ObservationPayload {
  dom: string;
  screenshot?: string; // base64 encoded PNG
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
