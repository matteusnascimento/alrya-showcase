export type RevenueSummary = {
  companyId: string;
  total: string;
};

export class ApiError extends Error {
  constructor(
    message: string,
    readonly status: number,
  ) {
    super(message);
    this.name = "ApiError";
  }
}

type FetchRevenueOptions = {
  companyId: string;
  accessToken: string;
  signal?: AbortSignal;
};

export async function fetchRevenueSummary({
  companyId,
  accessToken,
  signal,
}: FetchRevenueOptions): Promise<RevenueSummary> {
  const response = await fetch(
    `/api/demo/companies/${encodeURIComponent(companyId)}/revenue`,
    {
      method: "GET",
      headers: {
        Accept: "application/json",
        Authorization: `Bearer ${accessToken}`,
        "X-Company-ID": companyId,
      },
      signal,
    },
  );

  if (!response.ok) {
    throw new ApiError(
      `Revenue request failed with status ${response.status}`,
      response.status,
    );
  }

  const payload = (await response.json()) as {
    company_id: string;
    total: string | number;
  };

  return {
    companyId: payload.company_id,
    total: String(payload.total),
  };
}
