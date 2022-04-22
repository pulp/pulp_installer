describe port(80) do
  it { should be_listening }
end

describe port(443) do
  it { should be_listening }
end

describe http('http://localhost/pulp/api/v3/status/',
               ssl_verify: false) do
    its('status') { should eq 301 }
end

describe http('http://localhost/pulp/api/v3/status/',
               ssl_verify: false, max_redirects: 1) do
    its('status') { should eq 200 }
    its('body') { should match /database_connection/ }
end

describe http('https://localhost/pulp/api/v3/status/',
               ssl_verify: false) do
    its('status') { should eq 200 }
    its('body') { should match /database_connection/ }
end
